import numpy as np

from src.library.source.source import Source, DEFAULT_SAMPLE_RATE


class Generator(Source):
    def __init__(self, frequency: float = 440.0, duration: float = 1.0):
        super().__init__()
        self.frequency = frequency
        self.duration = duration

    def get_wave(self, start_time_s=0, end_time_s=10):
        if end_time_s > self.duration:
            raise Exception("Requested wave end time is too large.")

        duration = end_time_s - start_time_s
        t = np.arange(0, duration, 1.0 / self.sample_rate)
        signal = np.sin(2 * np.pi * self.frequency * t)

        return signal
