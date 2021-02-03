from tempfile import NamedTemporaryFile

import numpy as np
import pytest

from src.dsp.wave import Wave
from src.sources.trig_generators import generate_sine


@pytest.mark.parametrize("frequency", [10, 50, 420, 1000, 20000])
@pytest.mark.parametrize("duration", [0.1, 0.5, 2])
def test_generate_sine(frequency: float, duration: float):
    # Attempt to write a sine wave to a file, and read back the same data.
    wave = generate_sine(frequency, 0, duration)

    with NamedTemporaryFile(suffix=".wav") as f:
        file_location = f.name
        wave.write_to_file(file_location)
        read_wave = Wave.load_from_file(file_location)

        np.testing.assert_array_almost_equal(read_wave.signal, wave.signal)
