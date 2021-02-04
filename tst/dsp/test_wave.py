from tempfile import NamedTemporaryFile

import numpy as np
import pytest

from src.dsp.wave import Wave
from src.sources.shape_generators import generate_sine


@pytest.mark.parametrize("frequency", [10, 50, 420, 1000, 20000])
@pytest.mark.parametrize("duration", [0.1, 0.5, 2])
def test_save_and_load(frequency: float, duration: float):
    # Attempt to write a sine wave to a file, and read back the same data.
    wave = generate_sine(frequency, 0, duration)

    with NamedTemporaryFile(suffix=".wav") as f:
        file_location = f.name
        wave.write_to_file(file_location)
        read_wave = Wave.load_from_file(file_location)

        np.testing.assert_array_almost_equal(read_wave.signal, wave.signal)


@pytest.mark.parametrize("start_time_s", [0, 0.4, 1])
@pytest.mark.parametrize("end_time_s", [0, 0.5, 1])
def test_crop(start_time_s: float, end_time_s: float):
    wave = generate_sine(frequency=440, offset_time_s=0, duration_s=1.0)
    cropped_wave = wave.crop(start_time_s, end_time_s)

    expected_duration = np.clip(end_time_s - start_time_s, 0, wave.time_s)
    np.testing.assert_almost_equal(cropped_wave.time_s, expected_duration)
