import numpy as np

from src.interpreter.graph_type import GraphType


class Wave(GraphType):
    def __init__(self, signal: np.ndarray, sample_rate: int):
        self.signal = signal
        self.sample_rate = sample_rate

    @property
    def time_seconds(self) -> float:
        return float(self.number_of_samples / self.sample_rate)

    @property
    def number_of_samples(self) -> int:
        return len(self.signal)
