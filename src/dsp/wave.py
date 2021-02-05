from typing import Optional

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile

from src.util import constants


class Wave:
    """
    Contains a timeseries of audio samplings, and a variety of methods for generic signal analysis.
    """

    def __init__(self, signal: np.ndarray, sample_rate: int):
        self.signal = np.clip(
            signal, constants.MINIMUM_WAVE_SIGNAL_VALUE, constants.MAXIMUM_WAVE_SIGNAL_VALUE
        )
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
    def load_from_file(
        cls,
        file_location: str,
        duration_s: Optional[float] = None,
        sample_rate: int = constants.DEFAULT_SAMPLE_RATE,
    ):

        wave_array, _ = librosa.load(file_location, sr=sample_rate, duration=duration_s)

        return cls(wave_array, sample_rate)

    ################################################################################################

    def crop(
        self, start_time_s: Optional[float] = None, end_time_s: Optional[float] = None
    ) -> "Wave":
        start_sample = 0
        if start_time_s is not None:
            start_sample = self.sample_at_time(start_time_s)

        end_sample = self.sample_count - 1
        if end_time_s is not None:
            end_sample = self.sample_at_time(end_time_s)

        if end_sample <= start_sample:
            signal = np.array([])
        else:
            signal = self.signal[start_sample:end_sample]

        return self.__class__(signal, self.sample_rate)

    def sample_at_time(self, cursor_s: float) -> int:
        timestamp_ratio = np.clip(cursor_s / self.time_s, 0.0, 1.0)
        return int(self.sample_count * timestamp_ratio)

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
