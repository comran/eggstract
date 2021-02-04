import numpy as np

from src.dsp.mix import Mix
from src.sources import shape_generators
from src.util import constants


def test_mix():
    wave_one = shape_generators.generate_sine(100, 0, 1)
    wave_two = shape_generators.generate_sine(100, 0, 1)

    wave_one.signal *= 0.5
    wave_two.signal *= 0.5

    # Adding these two signals together should yield a sine wave with amplitude 1.
    mix_1 = Mix([wave_one, wave_two])
    np.testing.assert_array_almost_equal(mix_1.wave.signal, 2 * wave_one.signal, decimal=2)

    # Inverting one of the signals and mixing should cancel them out.
    wave_one.signal *= -1

    mix_2 = Mix([wave_one, wave_two])
    np.testing.assert_array_almost_equal(
        mix_2.wave.signal, np.zeros(wave_one.sample_count), decimal=2
    )


def test_mix_resample():
    """
    Creates a mix out of two signals that have different sampling rates.
    """

    wave_one = shape_generators.generate_sine(100, 0, 1, constants.DEFAULT_SAMPLE_RATE)
    wave_two = shape_generators.generate_sine(100, 0, 1, constants.DEFAULT_SAMPLE_RATE * 1.3)

    wave_one.signal *= 0.5
    wave_two.signal *= 0.5

    # Adding these two signals together should yield a sine wave with amplitude 1.
    mix_1 = Mix([wave_one, wave_two], sample_rate=constants.DEFAULT_SAMPLE_RATE)
    np.testing.assert_equal(mix_1.sample_rate, constants.DEFAULT_SAMPLE_RATE)

    mix_1_wave = mix_1.wave
    np.testing.assert_array_almost_equal(mix_1_wave.signal, 2 * wave_one.signal, decimal=2)
