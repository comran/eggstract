import numpy as np
import pytest

from src.dsp.fft import Fft
from src.sources.trig_generators import generate_sine


@pytest.mark.parametrize("frequency", [10, 50, 420, 1000, 20000])
@pytest.mark.parametrize("duration", [0.1, 0.5, 2])
def test_generate_sine(frequency: float, duration: float):
    wave = generate_sine(frequency, 0, duration)
    signal = wave.signal
    sample_rate = wave.sample_rate

    np.testing.assert_almost_equal(len(signal), sample_rate * duration, decimal=2)

    # Verify that the peak frequency matches the desired frequency given to the constructor.
    largest_frequencies = Fft.from_wave(wave).frequencies_sorted()
    np.testing.assert_almost_equal(largest_frequencies[0], frequency, decimal=2)
