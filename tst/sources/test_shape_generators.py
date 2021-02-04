import numpy as np
import pytest

from src.dsp.fft import Fft
from src.sources import shape_generators

TEST_FREQUENCIES = [10, 50, 420, 1000, 20000]
TEST_DURATIONS = [0.1, 0.5, 2]


@pytest.mark.parametrize("frequency", TEST_FREQUENCIES)
@pytest.mark.parametrize("duration", TEST_DURATIONS)
def test_generate_sine(frequency: float, duration: float):
    wave = shape_generators.generate_sine(frequency, 0, duration)
    signal = wave.signal
    sample_rate = wave.sample_rate

    np.testing.assert_almost_equal(len(signal), sample_rate * duration, decimal=2)

    # Verify that the peak frequency matches the desired frequency given to the constructor.
    largest_frequencies = Fft.from_wave(wave).frequencies_sorted()
    np.testing.assert_almost_equal(largest_frequencies[0], frequency, decimal=2)


@pytest.mark.parametrize("frequency", TEST_FREQUENCIES)
@pytest.mark.parametrize("duration", TEST_DURATIONS)
def test_generate_square(frequency: float, duration: float):
    wave = shape_generators.generate_square(
        frequency=frequency, offset_time_s=0, duration_s=duration
    )

    np.testing.assert_almost_equal(len(wave.signal), wave.sample_rate * duration, decimal=2)


@pytest.mark.parametrize("frequency", TEST_FREQUENCIES)
@pytest.mark.parametrize("duration", TEST_DURATIONS)
@pytest.mark.parametrize("width", [0, 0.3, 1])
def test_generate_sawtooth(frequency: float, duration: float, width: float):
    wave = shape_generators.generate_sawtooth(
        frequency=frequency, width=width, offset_time_s=0, duration_s=duration
    )

    np.testing.assert_almost_equal(len(wave.signal), wave.sample_rate * duration, decimal=2)


@pytest.mark.parametrize("frequency", TEST_FREQUENCIES)
@pytest.mark.parametrize("duration", TEST_DURATIONS)
def test_generate_triangle(frequency: float, duration: float):
    wave = shape_generators.generate_triangle(
        frequency=frequency, offset_time_s=0, duration_s=duration
    )

    sawtooth_wave = shape_generators.generate_sawtooth(
        frequency=frequency, width=0.5, offset_time_s=0, duration_s=duration
    )

    np.testing.assert_almost_equal(len(wave.signal), wave.sample_rate * duration, decimal=2)
    np.testing.assert_array_almost_equal(wave.signal, sawtooth_wave.signal, decimal=2)
