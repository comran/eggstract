import numpy as np
import pytest

from src.library.source.noise_generator import NoiseGenerator


@pytest.mark.parametrize("duration", [10, 50.23, 100])
def test_get_signal(duration):
    noise_generator = NoiseGenerator(duration=duration)
    wave = noise_generator.get_wave(0, duration)
    sample_rate = noise_generator.get_sample_rate()

    np.testing.assert_almost_equal(len(wave), sample_rate * duration, decimal=2)
