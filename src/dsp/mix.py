from typing import List

import numpy as np
import scipy

from src.dsp.wave import Wave
from src.util import constants


class Mix:
    def __init__(self, sources: List[Wave], sample_rate: int = constants.DEFAULT_SAMPLE_RATE):
        self.sources = sources
        self.sample_rate = sample_rate

    @property
    def wave(self) -> Wave:
        duration_s = np.max([source.time_s for source in self.sources])
        mix_signal = np.zeros(int(self.sample_rate * duration_s))

        for source in self.sources:
            source_signal = source.signal
            source_sample_count = int(source.time_s * self.sample_rate)

            # Resample (if necessary)
            if source.sample_rate != self.sample_rate:
                source_signal = scipy.signal.resample(source_signal, source_sample_count)

            mix_signal[0:source_sample_count] += source_signal

        return Wave(mix_signal, self.sample_rate)
