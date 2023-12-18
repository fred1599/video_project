import json
import os
import subprocess
from typing import Any, Dict, List, Optional


class Video:
    def __init__(self, filepath: str):
        self.filepath: str = filepath
        self.format: Optional[str] = None
        self.metadata: Dict[str, Any] = {}
        self.duration: Optional[float] = None
        self.resolution: Optional[str] = None
        self.bitrate: Optional[int] = None
        self.audio_tracks: List[str] = []
        self.subtitles: List[str] = []
        self.codec: Optional[str] = None

        self.get_metadata()

    def get_metadata(self) -> None:
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

    def _parse_metadata(self, metadata: Dict[str, Any]) -> None:
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

    def convert(self, output_format: str, quality: str = "middle") -> Optional[str]:
        output_file = os.path.splitext(self.filepath)[0] + "." + output_format

        quality_settings = {
            "low": "35",
            "middle": "28",
            "high": "20",
        }
        crf = quality_settings.get(quality, "28")

        command = ["ffmpeg", "-i", self.filepath, "-crf", crf, output_file]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("Error during conversion:", result.stderr.decode())
            return None

        return output_file

    def repair(self) -> str:
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

    def extract_audio(self, audio_format: str) -> Optional[str]:
        output_file = os.path.splitext(self.filepath)[0] + "." + audio_format

        command = [
            "ffmpeg",
            "-i",
            self.filepath,
            "-vn",
            "-acodec",
            audio_format,
            output_file,
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("Error during audio extraction:", result.stderr.decode())
            return None

        return output_file


class VideoList:
    def __init__(self, video_list: List[Video]):
        self.video_list: List[Video] = video_list

    def convert_all(self, output_format: str) -> None:
        # Convert all videos in the list
        pass
