import numpy as np

from src.dsp.wave import Wave


class Fft:
    def __init__(self, frequencies: np.ndarray, amplitudes: np.ndarray):
        self.frequencies = frequencies
        self.amplitudes = amplitudes

    ################################################################################################

    @classmethod
    def from_wave(cls, wave: Wave):
        # Convert from time domain to frequency domain using a fast fourier transform.
        fft = np.fft.fft(wave.signal)

        # Extract amplitudes and frequencies from the fft results.
        amplitudes = 1 / wave.sample_count * np.abs(fft)
        frequencies = np.fft.fftfreq(wave.sample_count) * wave.sample_count / wave.time_s

        # Get one side of the frequency/amplitude ranges.
        frequencies = frequencies[: len(frequencies) // 2]
        amplitudes = amplitudes[: len(fft) // 2]

        return cls(frequencies, amplitudes)

    ################################################################################################

    def frequencies_sorted(self) -> np.ndarray:
        """
        Creates a list of frequencies that appear in the signal, sorted in decreasing order by their
        amplitude.
        """

        # Sort by amplitude.
        frequency_domain = np.column_stack((self.frequencies, self.amplitudes))
        frequency_domain = frequency_domain[((-frequency_domain[:, 1]).argsort())]

        # Return largest frequencies.
        return frequency_domain[:, 0]
