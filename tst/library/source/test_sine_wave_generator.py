import numpy as np
import pytest

from src.library.source.sine_wave_generator import SineWaveGenerator
from src.util.audio_tools import find_largest_frequencies


@pytest.mark.parametrize("frequency", [10, 50, 420, 1000, 20000])
@pytest.mark.parametrize("duration", [0.1, 0.5, 2])
def test_get_signal(frequency, duration):
    sine_wave_generator = SineWaveGenerator(frequency=frequency, duration=duration)
    wave = sine_wave_generator.get_wave(0, duration)
    sample_rate = sine_wave_generator.get_sample_rate()

    np.testing.assert_almost_equal(len(wave), sample_rate * duration, decimal=2)

    # Verify that the peak frequency matches the desired frequency given to the constructor.
    largest_frequencies = find_largest_frequencies(wave, sample_rate)
    np.testing.assert_almost_equal(largest_frequencies[0], frequency, decimal=2)
