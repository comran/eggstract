import numpy as np

from src.library.source.source import Source


class NoiseGenerator(Source):
    def __init__(self, duration: float = 1.0):
        super().__init__()

        self.duration = duration

    def get_wave(self, start_time_s=0, duration=10):
        end_time_s = start_time_s + duration
        if end_time_s > self.duration:
            raise Exception("Requested wave end time is too large.")

        number_of_samples = int(duration * self.sample_rate)

        return np.random.rand(number_of_samples)
