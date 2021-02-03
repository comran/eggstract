import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


class Wave:
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

    def frequencies(self) -> np.ndarray:
        """
        Creates a list of frequencies that appear in the signal, sorted in decreasing order by their
        amplitude.
        """

        # Convert from time domain to frequency domain using a fast fourier transform.
        fft = np.fft.fft(self.signal)

        # Extract amplitudes and frequencies from the fft results.
        amplitudes = 1 / self.sample_count * np.abs(fft)
        frequencies = np.fft.fftfreq(self.sample_count) * self.sample_count / self.time_s

        # Get one side of the frequency/amplitude ranges.
        frequencies = frequencies[: len(frequencies) // 2]
        amplitudes = amplitudes[: len(fft) // 2]

        # Stack the result, and sort by frequency.
        frequency_domain = np.column_stack((frequencies, amplitudes))
        frequency_domain = frequency_domain[((-frequency_domain[:, 1]).argsort())]

        # Return largest frequencies.
        return np.array(frequency_domain[:, 0])

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
