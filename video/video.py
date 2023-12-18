import json
import os
import subprocess


class Video:
    def __init__(self, filepath):
        self.filepath = filepath
        self.format = None
        self.metadata = {}
        self.duration = None
        self.resolution = None
        self.bitrate = None
        self.audio_tracks = []
        self.subtitles = []
        self.codec = None

        self.get_metadata()

    def get_metadata(self):
        command = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            self.filepath,
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        metadata = json.loads(result.stdout)
        self.metadata = metadata
        self._parse_metadata(metadata)

    def _parse_metadata(self, metadata):
        """Parses the metadata and assigns values to the class attributes"""
        if "format" in metadata:
            self.format = metadata["format"].get("format_name")
            self.duration = float(metadata["format"].get("duration", 0.0))
            self.bitrate = int(metadata["format"].get("bit_rate", 0))

        for stream in metadata.get("streams", []):
            if stream["codec_type"] == "video":
                self.resolution = f"{stream.get('width')}x{stream.get('height')}"
                self.codec = stream.get("codec_name")
            elif stream["codec_type"] == "audio":
                self.audio_tracks.append(stream.get("codec_name"))
            elif stream["codec_type"] == "subtitle":
                self.subtitles.append(stream.get("codec_name"))

    def convert(self, output_format, quality="middle"):
        output_file = os.path.splitext(self.filepath)[0] + "." + output_format

        # Paramètres de qualité
        quality_settings = {
            "low": "35",  # CRF plus élevé signifie une qualité inférieure
            "middle": "28",
            "high": "20",  # CRF plus bas signifie une meilleure qualité
        }
        crf = quality_settings.get(quality, "28")  # Valeur par défaut pour middle

        command = ["ffmpeg", "-i", self.filepath, "-crf", crf, output_file]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("Erreur lors de la conversion :", result.stderr.decode())
            return None

        return output_file

    def repair(self):
        output_file = self.filepath.rsplit(".", 1)[0] + "_repaired.mp4"
        command = [
            "ffmpeg",
            "-err_detect",
            "ignore_err",
            "-i",
            self.filepath,
            "-c",
            "copy",
            output_file,
        ]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_file

    def extract_audio(self, audio_format):
        output_file = os.path.splitext(self.filepath)[0] + "." + audio_format

        command = [
            "ffmpeg",
            "-i",
            self.filepath,
            "-vn",  # Désactive la partie vidéo
            "-acodec",
            audio_format,  # Spécifie le codec audio
            output_file,
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("Error during audio extraction:", result.stderr.decode())
            return None

        return output_file


# Classe pour gérer une liste de vidéos
class VideoList:
    def __init__(self, video_list):
        self.video_list = video_list

    def convert_all(self, output_format):
        # Convertir toutes les vidéos de la liste
        pass
