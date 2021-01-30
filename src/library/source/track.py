import librosa

from src.util.crypto import get_file_sha256
from src.util.constants import DEFAULT_SAMPLE_RATE
from src.util.audio_tools import load_wave_from_file


class Track:
    def __init__(self, file_location: str):
        self.file_location = file_location
        self.sha256 = get_file_sha256(file_location)
        self.sample_rate = DEFAULT_SAMPLE_RATE

    def get_hash(self) -> str:
        return self.sha256

    def get_wave(self):
        return load_wave_from_file(self.file_location, self.sample_rate)
