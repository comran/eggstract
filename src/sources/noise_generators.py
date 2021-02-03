import numpy as np

from src.dsp.wave import Wave
from src.util.constants import DEFAULT_SAMPLE_RATE


def generate_random_noise(duration_s: float = 1.0, sample_rate: int = DEFAULT_SAMPLE_RATE) -> Wave:
    number_of_samples = int(duration_s * sample_rate)
    signal = np.random.rand(number_of_samples)
    wave = Wave(signal, sample_rate)

    return wave
