import pytest

from src.analysis import hearing_model
from src.util import constants

FREQUENCY_PARAMETERIZATIONS = [
    (0, None),
    (23.4, constants.FREQUENCY_SPECTRUM_CLASSIFICATIONS[0]),
    (40, constants.FREQUENCY_SPECTRUM_CLASSIFICATIONS[1]),
    (85, constants.FREQUENCY_SPECTRUM_CLASSIFICATIONS[2]),
    (250, constants.FREQUENCY_SPECTRUM_CLASSIFICATIONS[3]),
    (320, constants.FREQUENCY_SPECTRUM_CLASSIFICATIONS[4]),
    (652, constants.FREQUENCY_SPECTRUM_CLASSIFICATIONS[5]),
    (2450, constants.FREQUENCY_SPECTRUM_CLASSIFICATIONS[6]),
    (4900, constants.FREQUENCY_SPECTRUM_CLASSIFICATIONS[7]),
    (19999.999, constants.FREQUENCY_SPECTRUM_CLASSIFICATIONS[9]),
    (20000, None),
    (50000, None),
]


@pytest.mark.parametrize("frequency, expected_classification", FREQUENCY_PARAMETERIZATIONS)
def test_frequency_description(frequency, expected_classification):
    if expected_classification is None:
        assert hearing_model.frequency_description(frequency) == expected_classification
    else:
        assert (
            hearing_model.frequency_description(frequency) == expected_classification["description"]
        )


@pytest.mark.parametrize("frequency, expected_classification", FREQUENCY_PARAMETERIZATIONS)
def test_frequency_caution(frequency, expected_classification):
    if expected_classification is None:
        assert hearing_model.frequency_caution(frequency) == expected_classification
    else:
        assert hearing_model.frequency_caution(frequency) == expected_classification["caution"]


@pytest.mark.parametrize("frequency, expected_classification", FREQUENCY_PARAMETERIZATIONS)
def test_frequency_octave(frequency, expected_classification):
    if expected_classification is None:
        assert hearing_model.frequency_octave(frequency) == expected_classification
    else:
        assert hearing_model.frequency_octave(frequency) == expected_classification["octave"]
