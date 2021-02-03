import numpy as np

from src.dsp.wave import Wave
from src.util.constants import DEFAULT_SAMPLE_RATE


def generate_sine(
    frequency: int,
    offset_time_s: float = 0,
    duration_s: float = 1.0,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
) -> Wave:

    t = np.arange(offset_time_s, duration_s + offset_time_s, 1.0 / sample_rate)
    signal = np.sin(2 * np.pi * frequency * t)

    return Wave(signal, sample_rate)
