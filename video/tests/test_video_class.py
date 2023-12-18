import unittest
from typing import Any, Dict
from unittest.mock import MagicMock, patch

from video.video import Video


class TestVideo(unittest.TestCase):
    def setUp(self) -> None:
        self.test_video_path: str = "test_video.mp4"
        self.test_video: Video = Video(self.test_video_path)

    @patch("subprocess.run")
    def test_get_metadata(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(stdout=b'{"format": {}, "streams": []}')
        self.test_video.get_metadata()
        mock_run.assert_called()
        self.assertIsNotNone(self.test_video.metadata)

    def test_parse_metadata(self) -> None:
        fake_metadata: Dict[str, Any] = {
            "format": {"format_name": "mp4", "duration": "100.0", "bit_rate": "1000"},
            "streams": [
                {
                    "codec_type": "video",
                    "width": 1920,
                    "height": 1080,
                    "codec_name": "h264",
                },
                {"codec_type": "audio", "codec_name": "aac"},
                {"codec_type": "subtitle", "codec_name": "srt"},
            ],
        }
        self.test_video._parse_metadata(fake_metadata)
        self.assertEqual(self.test_video.format, "mp4")
        self.assertEqual(self.test_video.duration, 100.0)
        self.assertEqual(self.test_video.bitrate, 1000)
        self.assertEqual(self.test_video.resolution, "1920x1080")
        self.assertIn("aac", self.test_video.audio_tracks)
        self.assertIn("srt", self.test_video.subtitles)

    @patch("subprocess.run")
    def test_convert(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=0)
        output_file = self.test_video.convert("avi", "low")
        mock_run.assert_called()
        if output_file is not None:
            self.assertIn(".avi", output_file)

    @patch("subprocess.run")
    def test_repair(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=0)
        output_file = self.test_video.repair()
        mock_run.assert_called()
        if output_file is not None:
            self.assertIn("_repaired.mp4", output_file)

    @patch("subprocess.run")
    def test_extract_audio(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=0)
        output_file = self.test_video.extract_audio("mp3")
        mock_run.assert_called()
        if output_file is not None:
            self.assertIn(".mp3", output_file)


if __name__ == "__main__":
    unittest.main()
