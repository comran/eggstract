from abc import ABC, abstractmethod
from scipy.io.wavfile import write
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

DEFAULT_SAMPLE_RATE = 44100


class Source(ABC):
    def __init__(self):
        self.sample_rate = DEFAULT_SAMPLE_RATE

    @abstractmethod
    def get_wave(self, start_time_s=0, end_time_s=1):
        pass

    def get_sample_rate(self):
        return self.sample_rate

    def write_to_file(self, file_location: str):
        wave = (self.get_wave() * np.power(2, 15)).astype(np.int16)
        write(file_location, self.sample_rate, wave)

    def display_wave(self):
        wave = self.get_wave()
        # plt.figure(figsize=(14, 5))
        # librosa.display.waveplot(wave, sr=self.sample_rate)
        # plt.show()

        X = librosa.stft(wave)
        Xdb = librosa.amplitude_to_db(abs(X))
        plt.figure(figsize=(14, 5))
        librosa.display.specshow(Xdb, sr=self.sample_rate, x_axis="time", y_axis="hz")
        plt.colorbar()
        plt.show()
