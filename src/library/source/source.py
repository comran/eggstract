from abc import ABC, abstractmethod
from scipy.io.wavfile import write
import numpy as np

from src.util.constants import DEFAULT_SAMPLE_RATE
from src.util import audio_tools


class Source(ABC):
    def __init__(self):
        self.sample_rate = DEFAULT_SAMPLE_RATE

    @abstractmethod
    def get_wave(self, start_time_s=0, end_time_s=1):
        pass

    def get_sample_rate(self):
        return self.sample_rate

    def write_to_file(self, file_location: str):
        audio_tools.write_wave_to_file(file_location, self.get_wave(), self.get_sample_rate())

    def display_wave(self):
        audio_tools.display_wave(self.get_wave(), self.get_sample_rate())

    def display_spectrum(self):
        audio_tools.display_spectrum(self.get_wave(), self.get_sample_rate())
