import pytest
import numpy as np

from src.analysis.beat import bpm
from src.dsp.wave import Wave
from src.util import constants


@pytest.mark.skipif(constants.TRAVIS, reason=constants.TRAVIS_SKIP_REASON)
def test_eggstract():
    test_track = (
        f"{constants.LIBRARY_AUDIO_ROOT}/9a32b234e3514e92013efdec08d6bda152f5a0d6dbc37cf"
        "5f048558c0ad264cc.mp3"
    )

    track_wave = Wave.load_from_file(test_track)
    estimated_bpm = bpm.find_bpm(track_wave)
    np.testing.assert_approx_equal(estimated_bpm, 130, significant=2)
