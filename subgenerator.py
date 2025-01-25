import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import whisper

# Conditionally import faster_whisper if available/needed.
try:
    from faster_whisper import WhisperModel as FasterWhisperModel
except ImportError:
    FasterWhisperModel = None


def convert_to_srt(segments, progress_callback=None):
    """
    Convert transcription segments to SRT format.
    Optionally update an individual file progress bar via progress_callback.
    """
    # If segments is a generator or otherwise not indexable, convert to list.
    if not hasattr(segments, '__getitem__'):
        segments = list(segments)
    
    def format_timestamp(t):
        # Format time in HH:MM:SS,mmm
        hours = int(t // 3600)
        minutes = int((t % 3600) // 60)
        seconds = int(t % 60)
        milliseconds = int((t - int(t)) * 1000)
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    srt_lines = []
    total_segments = len(segments)
    for i, segment in enumerate(segments, start=1):
        # Standard Whisper => segment is a dict with "start", "end", "text".
        # Faster Whisper (with or without VAD) => can be a tuple (start, end, text, ...) or a Segment object.
        if isinstance(segment, dict):
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]
        elif isinstance(segment, (tuple, list)):
            # Some VAD outputs may have more than three items, so unpack only the first three.
            start, end, text, *rest = segment
        else:
            # If it's a Segment object, use segment.start, segment.end, segment.text
            start = segment.start
            end = segment.end
            text = segment.text

        srt_lines.append(f"{i}")
        srt_lines.append(f"{format_timestamp(start)} --> {format_timestamp(end)}")
        srt_lines.append(text.strip())
        srt_lines.append("")  # blank line

        if progress_callback:
            progress_callback(i, total_segments)

    return "\n".join(srt_lines)


class SubtitleGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video to SRT Subtitle Generator (Whisper/Faster Whisper)")
        self.video_files = []
        self.model = None  # Loaded model (Whisper or Faster Whisper)
        self.use_faster = tk.BooleanVar(value=False)
        self.use_word_timestamps = tk.BooleanVar(value=False)
        self.create_widgets()
        self.update_generate_button_state()

    def create_widgets(self):
        # File selection frame
        file_frame = tk.LabelFrame(self.root, text="Video Files")
        file_frame.pack(fill="x", padx=10, pady=5)

        self.file_listbox = tk.Listbox(file_frame, height=6, selectmode=tk.SINGLE)
        self.file_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        file_btn_frame = tk.Frame(file_frame)
        file_btn_frame.pack(side="right", padx=5, pady=5, fill="y")
        add_btn = tk.Button(file_btn_frame, text="Add Files", command=self.add_files)
        add_btn.pack(fill="x", pady=2)
        remove_btn = tk.Button(file_btn_frame, text="Remove Selected", command=self.remove_selected)
        remove_btn.pack(fill="x", pady=2)
        clear_btn = tk.Button(file_btn_frame, text="Clear All", command=self.clear_files)
        clear_btn.pack(fill="x", pady=2)

        # Model selection frame
        model_frame = tk.LabelFrame(self.root, text="Whisper Model")
        model_frame.pack(fill="x", padx=10, pady=5)
        self.model_var = tk.StringVar()
        self.model_combobox = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            state="readonly",
            values=["tiny", "base", "small", "medium", "large"]
        )
        self.model_combobox.current(1)  # Default to "base"
        self.model_combobox.pack(padx=5, pady=5)

        # Faster Whisper selection
        faster_frame = tk.LabelFrame(self.root, text="Faster Whisper Options")
        faster_frame.pack(fill="x", padx=10, pady=(2, 5))
        self.faster_checkbox = tk.Checkbutton(
            faster_frame,
            text="Use Faster Whisper (with VAD)",
            variable=self.use_faster,
            onvalue=True,
            offvalue=False,
            command=self.toggle_word_timestamp_checkbox  # update state of word-timestamp option
        )
        self.faster_checkbox.pack(anchor="w", padx=5, pady=2)

        # Word-level timestamp option
        self.word_timestamp_checkbox = tk.Checkbutton(
            faster_frame,
            text="Use Word-Level Timestamps",
            variable=self.use_word_timestamps,
            onvalue=True,
            offvalue=False
        )
        # Disabled by default; only enabled if Faster Whisper is selected.
        self.word_timestamp_checkbox.config(state=tk.DISABLED)
        self.word_timestamp_checkbox.pack(anchor="w", padx=25, pady=2)

        # Overall progress bar
        overall_progress_frame = tk.Frame(self.root)
        overall_progress_frame.pack(fill="x", padx=10, pady=(5, 2))
        tk.Label(overall_progress_frame, text="Overall Progress:").pack(anchor="w", padx=5)
        self.overall_progress_bar = ttk.Progressbar(overall_progress_frame, orient="horizontal", mode="determinate")
        self.overall_progress_bar.pack(fill="x", padx=5, pady=2)

        # Per-file progress bar
        file_progress_frame = tk.Frame(self.root)
        file_progress_frame.pack(fill="x", padx=10, pady=(2, 5))
        tk.Label(file_progress_frame, text="File Progress:").pack(anchor="w", padx=5)
        self.file_progress_bar = ttk.Progressbar(file_progress_frame, orient="horizontal", mode="determinate")
        self.file_progress_bar.pack(fill="x", padx=5, pady=2)

        # Process button and status label
        process_frame = tk.Frame(self.root)
        process_frame.pack(fill="x", padx=10, pady=5)
        self.process_btn = tk.Button(process_frame, text="Generate Subtitles", command=self.start_processing)
        self.process_btn.pack(pady=5)
        self.status_label = tk.Label(self.root, text="Status: Waiting", anchor="w")
        self.status_label.pack(fill="x", padx=10, pady=5)

    def toggle_word_timestamp_checkbox(self):
        """Enable or disable the word-level timestamp option based on use_faster."""
        if self.use_faster.get():
            self.word_timestamp_checkbox.config(state=tk.NORMAL)
        else:
            self.word_timestamp_checkbox.config(state=tk.DISABLED)
            self.use_word_timestamps.set(False)

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select Video Files",
            filetypes=[("Video Files", "*.mp4 *.mov *.mkv *.avi *.flv"), ("All Files", "*.*")]
        )
        if files:
            for file in files:
                if file not in self.video_files:
                    self.video_files.append(file)
                    self.file_listbox.insert(tk.END, file)
            self.update_generate_button_state()

    def remove_selected(self):
        selected_indices = list(self.file_listbox.curselection())
        selected_indices.sort(reverse=True)
        for index in selected_indices:
            self.video_files.pop(index)
            self.file_listbox.delete(index)
        self.update_generate_button_state()

    def clear_files(self):
        self.video_files.clear()
        self.file_listbox.delete(0, tk.END)
        self.update_generate_button_state()

    def update_generate_button_state(self):
        # Enable the Generate Subtitles button only if there are video files.
        if self.video_files:
            self.process_btn.config(state=tk.NORMAL)
        else:
            self.process_btn.config(state=tk.DISABLED)

    def start_processing(self):
        if not self.video_files:
            messagebox.showwarning("No Files Selected", "Please add at least one video file.")
            return

        model_name = self.model_var.get()
        use_faster = self.use_faster.get()

        if use_faster and not FasterWhisperModel:
            messagebox.showerror("Missing Package", "Faster Whisper package is not installed.")
            return

        self.process_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Loading model...")
        self.overall_progress_bar["maximum"] = len(self.video_files)
        self.overall_progress_bar["value"] = 0

        threading.Thread(target=self.process_files, args=(model_name, use_faster), daemon=True).start()

    def process_files(self, model_name, use_faster):
        errors = []
        total_files = len(self.video_files)
        current_file_num = 0

        # Load the model once (either standard Whisper or Faster Whisper).
        try:
            if use_faster:
                # Create a Faster Whisper model instance.
                self.model = FasterWhisperModel(model_name, device="cpu")
            else:
                self.model = whisper.load_model(model_name)
        except Exception as e:
            self.update_status(f"Error loading model: {str(e)}")
            self.process_btn.config(state=tk.NORMAL)
            return

        for file in self.video_files:
            current_file_num += 1
            base_name = os.path.basename(file)
            self.update_status(f"Processing ({current_file_num}/{total_files}): {base_name}")
            self.file_progress_bar["value"] = 0

            try:
                if use_faster:
                    # For VAD, transcribe returns (segments, info).
                    # If word-level timestamps are enabled, pass word_timestamps=True.
                    if self.use_word_timestamps.get():
                        segments_generator, info = self.model.transcribe(
                            file, 
                            beam_size=5, 
                            vad_filter=True, 
                            word_timestamps=True
                        )
                    else:
                        segments_generator, info = self.model.transcribe(
                            file, 
                            beam_size=5, 
                            vad_filter=True
                        )
                    segments = list(segments_generator)  # Force generator into a list
                else:
                    # Standard Whisper transcription
                    result = self.model.transcribe(file, task='transcribe')
                    segments = result["segments"]

                def update_file_progress(current, total):
                    self.file_progress_bar["maximum"] = total
                    self.file_progress_bar["value"] = current

                srt_content = convert_to_srt(segments, progress_callback=update_file_progress)
                output_path = os.path.splitext(file)[0] + ".srt"
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(srt_content)
            except Exception as e:
                errors.append(f"{base_name}: {str(e)}")

            self.overall_progress_bar["value"] = current_file_num

        self.update_status("Processing complete!")
        self.process_btn.config(state=tk.NORMAL)
        if errors:
            messagebox.showerror("Errors Occurred", "\n".join(errors))
        else:
            messagebox.showinfo("Done", "Subtitles were successfully generated for all videos.")

    def update_status(self, text):
        self.status_label.config(text=f"Status: {text}")


def main():
    root = tk.Tk()
    app = SubtitleGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
