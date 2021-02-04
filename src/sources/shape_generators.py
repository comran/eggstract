import numpy as np
import scipy

from src.dsp.wave import Wave
from src.util.constants import DEFAULT_SAMPLE_RATE


def radian_timeseries(frequency: float, duration_s: float, offset_time_s: float, sample_rate: int) -> np.ndarray:
    t = np.arange(offset_time_s, duration_s + offset_time_s, 1.0 / sample_rate)
    return 2 * np.pi * frequency * t


def generate_sine(
    frequency: int,
    offset_time_s: float = 0,
    duration_s: float = 1.0,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
) -> Wave:

    timeseries = radian_timeseries(frequency, duration_s, offset_time_s, sample_rate)
    signal = np.sin(timeseries)

    return Wave(signal, sample_rate)


def generate_square(
    frequency: int,
    duty_cycle: float = 0.5,
    offset_time_s: float = 0,
    duration_s: float = 1.0,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
) -> Wave:

    duty_cycle = np.clip(duty_cycle, 0, 1)

    timeseries = radian_timeseries(frequency, duration_s, offset_time_s, sample_rate)
    signal = scipy.signal.square(timeseries)

    return Wave(signal, sample_rate)
