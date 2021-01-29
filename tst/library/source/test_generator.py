import numpy as np
import pytest

from src.library.source.generator import Generator
from src.util.audio_tools import find_largest_frequencies


@pytest.mark.parametrize(
    "frequency",
    [10, 50, 420, 1000, 20000],
)
def test_get_signal(frequency):
    generator = Generator(frequency=frequency, duration=10.0)
    wave = generator.get_wave(0, 1)
    sample_rate = generator.get_sample_rate()

    assert wave.shape[0] == sample_rate

    largest_frequencies = find_largest_frequencies(wave)
    np.testing.assert_almost_equal(largest_frequencies[0], frequency)
