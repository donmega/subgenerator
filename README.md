# Subtitle Generator GUI

This Python application provides a graphical user interface (GUI) for generating SRT subtitle files from video files. It utilizes either the standard `openai-whisper` library or the `faster-whisper` library (with Voice Activity Detection (VAD)) for audio transcription. The program supports batch processing of multiple video files and offers options for model selection and word-level timestamps (with Faster Whisper).

## Table of Contents

- [Key Features](#key-features)
- [Technical Details](#technical-details)
  - [Dependencies](#dependencies)
  - [Core Functionality](#core-functionality)
    - [`convert_to_srt`](#convert_to_srtsegments-progress_callbacknone)
    - [SubtitleGeneratorGUI Class](#subtitlegeneratorgui-class)
  - [Model Loading](#model-loading)
  - [Transcription](#transcription)
  - [Output](#output)
- [User Guide](#user-guide)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
  - [Using the GUI](#using-the-gui)
    - [Add Video Files](#add-video-files)
    - [Select Model](#select-model)
    - [Faster Whisper Option](#faster-whisper-option)
    - [Word-Level Timestamps](#word-level-timestamps)
    - [Generate Subtitles](#generate-subtitles)
    - [Progress](#progress)
    - [Status Updates](#status-updates)
    - [Output Files](#output-files)
    - [Removal/Clear](#removalclear)
- [Troubleshooting](#troubleshooting)
- [Notes](#notes)

---

## Key Features

- **Video File Input**: Select one or more video files (e.g., MP4, MOV, MKV, AVI) for subtitle generation.
- **Model Selection**: Choose from various `openai-whisper` models (`tiny`, `base`, `small`, `medium`, `large`) via a dropdown menu.
- **Faster Whisper Option**: Utilize `faster-whisper` for faster processing and built-in voice activity detection (VAD).
- **Word-Level Timestamps**: Generate more granular word-level timestamp information when using Faster Whisper.
- **Progress Tracking**: Monitor overall progress across all files and individual progress within each file.
- **Error Handling**: Automatically catch and report errors during model loading or transcription.
- **Clear Status Updates**: Receive real-time updates on the application's status, such as model loading, file processing, and completion.

## Technical Details

### Dependencies

- **tkinter**: For creating the graphical user interface.
- **whisper** (or **openai-whisper**): For audio transcription.
- **faster-whisper** (optional): For faster transcription with VAD.
- **os**, **threading**: Standard Python libraries for file system interaction and multithreading.

### Core Functionality

#### `convert_to_srt(segments, progress_callback=None)`

Converts transcription segments to SRT format. This function also accepts a `progress_callback` function, allowing it to update the progress of an individual file during processing.

#### `SubtitleGeneratorGUI` Class

The main application class that:

- Handles UI creation and user interactions.
- Loads the specified Whisper model.
- Processes video files and converts output to SRT files.
- Manages status updates and overall progress.
- Utilizes threading to prevent freezing the GUI while processing.

### Model Loading

Loads the selected `openai-whisper` or `faster-whisper` model when processing starts.

### Transcription

- Uses the chosen model (`openai-whisper` or `faster-whisper`) to transcribe the audio of the video files.
- `faster-whisper` is used with VAD (Voice Activity Detection), improving performance by only processing segments with speech.
- The word-level timestamp option can be enabled with `faster-whisper`.

### Output

Generates SRT subtitle files with the same base name as the input video file, saving them in the same directory.

## User Guide

### Installation

1. **Prerequisites**:
   - Ensure you have Python installed (3.7 or higher recommended).

2. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```
   *Assuming you have a `requirements.txt` file containing `openai-whisper` and/or `faster-whisper`.*

### Running the Application

Execute the Python script:

```bash
python your_script_name.py  # Replace with the name of the .py file.
```

A GUI window will open.

### Using the GUI

#### Add Video Files

- Click the **"Add Files"** button to select one or more video files.

#### Select Model

- Choose a Whisper model size (`tiny`, `base`, `small`, `medium`, `large`) from the dropdown menu.

#### Faster Whisper Option

- Check the **"Use Faster Whisper (with VAD)"** checkbox to utilize Faster Whisper for potentially faster and more accurate results.

#### Word-Level Timestamps

- If using Faster Whisper, check the **"Use Word-Level Timestamps"** checkbox for granular timestamps.

#### Generate Subtitles

- Click the **"Generate Subtitles"** button to start the transcription and subtitle generation process.

#### Progress

- **Overall Progress**: Shows the progress of all video files.
- **File Progress**: Shows the progress of the current video file.

#### Status Updates

- The **"Status"** label displays the current action being performed (e.g., model loading, processing files).

#### Output Files

- The generated SRT files will be saved in the same directory as the input video files with the same name.

#### Removal/Clear

- **Remove Selected**: Removes the currently selected file(s) from the list.
- **Clear All**: Removes all files from the file list.

## Troubleshooting

- **"Faster Whisper package is not installed"**:
  - Ensure you have the `faster-whisper` package installed:
    ```bash
    pip install faster-whisper
    ```

- **Errors during processing**:
  - Check the error message for clues about what went wrong. Possible issues could relate to file access, audio problems, or model-related errors.

- **No subtitles generated**:
  - If no audio is detected in the video file, no subtitles may be generated.

## Notes

- The **Faster Whisper** option with VAD may provide faster processing by only handling voice segments.
- The **Word-Level Timestamps** option generates more detailed subtitles but increases computational overhead when using Faster Whisper.
