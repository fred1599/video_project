import shutil
import sys
from typing import List

import typer

from .video import Video

SUPPORTED_AUDIO_FORMATS: List[str] = ["mp3", "aac", "wav", "ogg", "flac"]
SUPPORTED_VIDEO_FORMATS: List[str] = ["mp4", "avi", "mkv", "mov", "flv", "wmv"]


def is_tool_installed(name: str) -> bool:
    """Checks if a tool is installed"""
    return shutil.which(name) is not None


def print_colored(text: str, color: str) -> None:
    """Displays text in the specified color"""
    colors = {"red": "\033[91m", "green": "\033[92m"}
    reset = "\033[0m"
    print(f"{colors.get(color, '')}{text}{reset}")


def check_ffmpeg_and_ffprobe() -> None:
    """Checks if ffmpeg and ffprobe are installed"""
    if is_tool_installed("ffmpeg") and is_tool_installed("ffprobe"):
        print_colored("ffmpeg and ffprobe are correctly installed.", "green")
    else:
        print_colored("ffmpeg or ffprobe are not installed.", "red")
        sys.exit(1)


app = typer.Typer()


def convert_video(input: str, output: str, quality: str) -> None:
    video = Video(input)
    if output not in SUPPORTED_VIDEO_FORMATS:
        typer.echo(
            f"Unsupported video format. Supported formats: {', '.join(SUPPORTED_VIDEO_FORMATS)}"
        )
        raise typer.Exit()

    try:
        for line in video.convert(output, quality):
            typer.echo(line)
    except FileNotFoundError as e:
        typer.echo(str(e))
        raise typer.Exit()
    except Exception as e:
        typer.echo(f"An error occurred during conversion: {str(e)}")
        raise typer.Exit()


def repair_video(input: str) -> None:
    video = Video(input)
    repaired_file = video.repair()
    typer.echo(f"Repaired video saved as: {repaired_file}")


def extract_audio_from_video(input: str, output: str) -> None:
    video = Video(input)
    if output not in SUPPORTED_AUDIO_FORMATS:
        typer.echo(
            f"Unsupported audio format. Supported formats: {', '.join(SUPPORTED_AUDIO_FORMATS)}"
        )
        raise typer.Exit()

    extracted_audio = video.extract_audio(output)
    if extracted_audio:
        typer.echo(f"Extracted audio saved as: {extracted_audio}")
    else:
        typer.echo("Audio extraction failed.")


@app.command()  # type: ignore
def main(
    command: str = typer.Option(
        ...,
        "--command",
        "-c",
        help="Command to execute (convert, repair, extract_audio)",
    ),
    input: str = typer.Option(..., "--input", "-i", help="Path to the video file"),
    output: str = typer.Option(
        None, "--output", "-o", help="Output format for conversion or audio extraction"
    ),
    quality: str = typer.Option(
        "middle",
        "--quality",
        "-q",
        help="Quality of the conversion (low, middle, high)",
    ),
) -> None:
    if command == "convert":
        convert_video(input, output, quality)
    elif command == "repair":
        repair_video(input)
    elif command == "extract_audio":
        extract_audio_from_video(input, output)
    else:
        typer.echo(
            "Invalid command. Please use 'convert', 'repair', or 'extract_audio'."
        )


if __name__ == "__main__":
    check_ffmpeg_and_ffprobe()
    typer.run(main)
