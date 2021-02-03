from tempfile import NamedTemporaryFile

import numpy as np
import pytest

from src.sources.audio_file import load_from_file, write_to_file
from src.sources.trig_generators import generate_sine


@pytest.mark.parametrize("frequency", [10, 50, 420, 1000, 20000])
@pytest.mark.parametrize("duration", [0.1, 0.5, 2])
def test_generate_sine(frequency: float, duration: float):
    wave = generate_sine(frequency, 0, duration)

    with NamedTemporaryFile(suffix=".wav") as f:
        file_location = f.name
        write_to_file(wave, file_location)
        read_wave = load_from_file(file_location)

        np.testing.assert_array_almost_equal(read_wave.signal, wave.signal)
