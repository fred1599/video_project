# Video Processing Application

This application allows performing various operations on video files, such as format conversion, repair, and audio extraction.

## Installation

Ensure Python 3.10 and `ffmpeg` are installed on your system. If not, you can download and install them from their respective websites.

## Usage

The application is executed via the command line. Here are the different commands and options available:

### General Commands

- **Help**: To display help and see all available options, use:

`python3.10 -m video --help`


### Video Conversion

- **Convert a Video**: To convert a video to another format, use:

`python3.10 -m video --command convert --input <path_to_video> --output <output_format> [--quality <quality>]`

- `<path_to_video>`: Path of the source video file.
- `<output_format>`: Desired output format (e.g., mp4, avi).
- `<quality>`: Video quality (low, middle, high). Defaults to `middle`.

### Video Repair

- **Repair a Video**: To attempt to repair a corrupted video, use:

`python3.10 -m video --command repair --input <path_to_video>`

- `<path_to_video>`: Path of the video file to repair.

### Audio Extraction

- **Extract Audio from a Video**: To extract the audio track from a video, use:

`python3.10 -m video --command extract_audio --input <path_to_video> --output <audio_format>`

- `<path_to_video>`: Path of the source video file.
- `<audio_format>`: Desired audio format for extraction (e.g., mp3, wav).

## Supported Formats

- **Supported video formats**: mp4, avi, mkv, mov, flv, wmv.
- **Supported audio formats**: mp3, aac, wav, ogg, flac.

## Dependencies

- Python 3.10
- `ffmpeg`

