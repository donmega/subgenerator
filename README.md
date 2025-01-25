Description:

This Python application provides a graphical user interface (GUI) for generating SRT subtitle files from video files. It utilizes either the standard openai-whisper library or the faster-whisper library (with voice activity detection (VAD)) for audio transcription. The program supports batch processing of multiple video files and offers options for model selection and word-level timestamps (with Faster Whisper).

Key Features:

Video File Input: Allows users to select one or more video files (e.g., MP4, MOV, MKV, AVI) for subtitle generation.

Model Selection: Provides a dropdown menu to select from various openai-whisper models (tiny, base, small, medium, large).

Faster Whisper Option: Enables the use of faster-whisper for faster processing and built-in voice activity detection.

Word-Level Timestamps: With Faster Whisper, users can choose to generate word-level timestamp information (more granular).

Progress Tracking: Displays overall progress across all files, as well as individual progress within each file.

Error Handling: Catches and reports errors during model loading or transcription.

Clear Status Updates: Informs the user about the current status of the application, such as model loading, file processing, and completion.

Technical Details:

Dependencies:

tkinter: For creating the graphical user interface.

whisper (or openai-whisper): For audio transcription.

faster-whisper (optional): For faster transcription with VAD.

os, threading: Standard Python libraries for file system interaction and multithreading.

Core Functionality:

convert_to_srt(segments, progress_callback=None): Converts transcription segments to SRT format. This function also accepts a progress_callback function, allowing it to update the progress of an individual file during processing.

SubtitleGeneratorGUI Class: The main application class:

Handles UI creation and user interactions.

Loads the specified Whisper model.

Processes video files and converts output to SRT files.

Manages status updates and overall progress.

Uses threading to prevent freezing the GUI while processing.

Model Loading:

Loads the selected openai-whisper or faster-whisper model when processing starts.

Transcription:

Uses the chosen model (openai-whisper or faster-whisper) to transcribe the audio of the video files.

faster-whisper is used with VAD (voice activity detection), improving performance by only processing segments with speech.

The word-level timestamp option can be enabled with faster-whisper.

Output: Generates SRT subtitle files with the same base name as the input video file, saving them in the same directory.

User Guide:

Installation:

Ensure you have Python installed (3.7 or higher recommended).

Install the required packages using pip:

pip install -r requirements.txt
content_copy
download
Use code with caution.
Bash

(Assuming you have a requirements.txt file containing openai-whisper and/or faster-whisper)

Running the Application:

Execute the Python script.

python your_script_name.py #Replace with the name of the .py file.
content_copy
download
Use code with caution.
Bash

A GUI window will open.

Using the GUI:

Add Video Files: Click the "Add Files" button to select one or more video files.

Select Model: Choose a Whisper model size (tiny, base, small, medium, large) from the dropdown.

Faster Whisper Option: Check the "Use Faster Whisper (with VAD)" checkbox to use Faster Whisper for potentially faster and more accurate results.

Word-Level Timestamps: If using Faster Whisper, check the "Use Word-Level Timestamps" checkbox for granular timestamps.

Generate Subtitles: Click the "Generate Subtitles" button.

Progress:

The "Overall Progress" bar shows the progress of all video files.

The "File Progress" bar shows the progress of the current video file.

Status Updates: The "Status" label displays the current action being performed (e.g., model loading, processing files).

Output Files: The generated SRT files will be saved in the same directory as the input video files with the same name.

Removal/Clear: The "Remove Selected" button removes the currently selected file(s) and the "Clear All" button will remove all files from the file list.

Troubleshooting:

"Faster Whisper package is not installed": Make sure you have the faster-whisper package installed.

Errors during processing: Check the error message for clues about what went wrong. This could be related to file access, audio issues, or model problems.

If no audio is detected, no subtitles may be generated.

Notes:

The faster-whisper option with VAD may provide faster processing due to only processing voice segments.

The "Word-Level Timestamps" option generates more detailed subtitles but increases computational overhead with faster-whisper.

This documentation aims to provide a clear and comprehensive overview of the application, covering its functionality and how to use it effectively.
