import numpy as np
import pytest

from src.sources.noise_generators import generate_random_noise


@pytest.mark.parametrize("duration", [10, 50.23, 100])
def test_generate_random_noise(duration):
    wave = generate_random_noise(duration)

    sample_rate = wave.sample_rate
    signal = wave.signal

    np.testing.assert_almost_equal(len(signal), sample_rate * duration, decimal=2)
