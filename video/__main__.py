import subprocess
import platform
import sys
import typer

from .video import Video

SUPPORTED_AUDIO_FORMATS = ["mp3", "aac", "wav", "ogg", "flac"]
SUPPORTED_VIDEO_FORMATS = ["mp4", "avi", "mkv", "mov", "flv", "wmv"]


def is_tool_installed(name):
    """ Checks if a tool is installed """
    try:
        command = "where" if platform.system() == "Windows" else "which"
        subprocess.run([command, name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def print_colored(text, color):
    """ Displays text in the specified color """
    colors = {"red": "\033[91m", "green": "\033[92m"}
    reset = "\033[0m"
    print(f"{colors.get(color, '')}{text}{reset}")

def check_ffmpeg_and_ffprobe():
    """ Checks if ffmpeg and ffprobe are installed """
    if is_tool_installed("ffmpeg") and is_tool_installed("ffprobe"):
        print_colored("ffmpeg and ffprobe are correctly installed.", "green")
    else:
        print_colored("ffmpeg or ffprobe are not installed.", "red")
        sys.exit(1)

app = typer.Typer()

@app.command()
def main(
    command: str = typer.Option(..., "--command", "-c", help="Command to execute (repair or convert)"),
    input: str = typer.Option(..., "--input", "-i", help="Path to the video file"),
    output: str = typer.Option(None, "--output", "-o", help="Output format for conversion"),
    quality: str = typer.Option("middle", "--quality", "-q", help="Quality of the conversion (low, middle, high)")
):

    video = Video(input)
    
    if command == "convert":
        if output not in SUPPORTED_VIDEO_FORMATS:
            typer.echo(f"Unsupported video format. Supported formats: {', '.join(SUPPORTED_VIDEO_FORMATS)}")
            raise typer.Exit()

        converted_file = video.convert(output, quality)

        if converted_file:
            typer.echo(f"Video converted and saved as: {converted_file}")

        else:
            typer.echo("The conversion failed.")

    if command == "repair":
        repaired_file = video.repair()
        typer.echo(f"Repaired video saved as: {repaired_file}")

    if command == "extract_audio":
        if output not in SUPPORTED_AUDIO_FORMATS:
            typer.echo(f"Unsupported audio format. Supported formats: {', '.join(SUPPORTED_AUDIO_FORMATS)}")
            raise typer.Exit()

        extracted_audio = video.extract_audio(output)

        if extracted_audio:
            typer.echo(f"Extracted audio saved as: {extracted_audio}")

        else:
            typer.echo("Audio extraction failed.")

if __name__ == "__main__":
    check_ffmpeg_and_ffprobe()
    typer.run(main)
