import numpy as np
from typing import Optional

from src.library.source.source import Source


class SineWaveGenerator(Source):
    def __init__(self, frequency: float = 440.0, duration: float = 1.0):
        super().__init__()
        self.frequency = frequency
        self.duration = duration

    def get_wave(self, start_time_s: float = 0, duration: Optional[float] = None):
        if duration is None:
            duration = self.duration

        end_time_s = start_time_s + duration
        if end_time_s > self.duration:
            raise Exception(
                "Requested wave end time is too large: "
                f"end_time_s[{end_time_s}] > duration[{self.duration}]"
            )

        t = np.arange(start_time_s, end_time_s, 1.0 / self.sample_rate)
        signal = np.sin(2 * np.pi * self.frequency * t)

        return signal
