import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile

from src.util.constants import DEFAULT_SAMPLE_RATE


class Wave:
    """
    Contains a timeseries of audio samplings, and a variety of methods for generic signal analysis.
    """

    def __init__(self, signal: np.ndarray, sample_rate: int):
        self.signal = np.clip(signal, -1.0, 1.0)
        self.sample_rate = sample_rate

    ################################################################################################

    @property
    def sample_count(self) -> int:
        return len(self.signal)

    @property
    def time_s(self) -> float:
        return float(self.sample_count / self.sample_rate)

    ################################################################################################

    @classmethod
    def load_from_file(cls, file_location: str, sample_rate: int = DEFAULT_SAMPLE_RATE):
        wave_array, _ = librosa.load(file_location, sr=sample_rate)

        return cls(wave_array, sample_rate)

    ################################################################################################

    def display_signal(self):
        """
        Displays the waveform.
        """

        plt.figure(figsize=(14, 5))
        librosa.display.waveplot(self.signal, sr=self.sample_rate)
        plt.show()

    def display_spectrum(self):
        """
        Displays the spectrogram.
        """

        X = librosa.stft(self.signal)
        Xdb = librosa.amplitude_to_db(abs(X))
        plt.figure(figsize=(14, 5))
        librosa.display.specshow(Xdb, sr=self.sample_rate, x_axis="time", y_axis="hz")

        plt.colorbar()
        plt.show()

    def write_to_file(self, file_location: str):
        soundfile.write(file_location, self.signal, self.sample_rate, "PCM_24")
