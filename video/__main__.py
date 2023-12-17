import subprocess
import platform
import sys
import typer

from .video import Video

SUPPORTED_AUDIO_FORMATS = ["mp3", "aac", "wav", "ogg", "flac"]
SUPPORTED_VIDEO_FORMATS = ["mp4", "avi", "mkv", "mov", "flv", "wmv"]


def is_tool_installed(name):
    """ Vérifie si un outil est installé """
    try:
        command = "where" if platform.system() == "Windows" else "which"
        subprocess.run([command, name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def print_colored(text, color):
    """ Affiche le texte avec la couleur spécifiée """
    colors = {"red": "\033[91m", "green": "\033[92m"}
    reset = "\033[0m"
    print(f"{colors.get(color, '')}{text}{reset}")

def check_ffmpeg_and_ffprobe():
    """ Vérifie si ffmpeg et ffprobe sont installés """
    if is_tool_installed("ffmpeg") and is_tool_installed("ffprobe"):
        print_colored("ffmpeg et ffprobe sont installés correctement.", "green")
    else:
        print_colored("ffmpeg ou ffprobe ne sont pas installés.", "red")
        sys.exit(1)

app = typer.Typer()

@app.command()
def main(
    command: str = typer.Option(..., "--command", "-c", help="Commande à exécuter (repair ou convert)"),
    input: str = typer.Option(..., "--input", "-i", help="Chemin du fichier vidéo"),
    output: str = typer.Option(None, "--output", "-o", help="Format de sortie pour la conversion"),
    quality: str = typer.Option("middle", "--quality", "-q", help="Qualité de la conversion (low, middle, high)")
):

    video = Video(input)
    
    if command == "convert":
        if output not in SUPPORTED_VIDEO_FORMATS:
            typer.echo(f"Format vidéo non pris en charge. Formats pris en charge: {', '.join(SUPPORTED_VIDEO_FORMATS)}")
            raise typer.Exit()

        converted_file = video.convert(output, quality)

        if converted_file:
            typer.echo(f"Vidéo convertie enregistrée sous : {converted_file}")

        else:
            typer.echo("La conversion a échoué.")

    if command == "repair":
        repaired_file = video.repair()
        typer.echo(f"Vidéo réparée enregistrée sous : {repaired_file}")

    if command == "extract_audio":
        if output not in SUPPORTED_AUDIO_FORMATS:
            typer.echo(f"Format audio non pris en charge. Formats pris en charge: {', '.join(SUPPORTED_AUDIO_FORMATS)}")
            raise typer.Exit()

        extracted_audio = video.extract_audio(output)

        if extracted_audio:
            typer.echo(f"Audio extrait enregistré sous : {extracted_audio}")

        else:
            typer.echo("L'extraction de l'audio a échoué.")

if __name__ == "__main__":
    check_ffmpeg_and_ffprobe()
    typer.run(main)
