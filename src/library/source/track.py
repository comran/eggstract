import librosa

from src.util.crypto import get_file_sha256

DEFAULT_SAMPLE_RATE = 44100


class Track:
    def __init__(self, file_location: str):
        self.file_location = file_location
        self.sha256 = get_file_sha256(file_location)
        self.sample_rate = DEFAULT_SAMPLE_RATE

    def get_hash(self) -> str:
        return self.sha256

    def get_wave(self):
        x, _ = librosa.load(self.file_location, sr=self.sample_rate)
        return x
