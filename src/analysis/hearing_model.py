from typing import Any, Dict, Optional, cast

from src.util import constants


def frequency_classification(frequency: float) -> Optional[Dict[str, Any]]:
    for description in constants.FREQUENCY_SPECTRUM_CLASSIFICATIONS:
        lower_range_hz = cast(float, description["lower_range_hz"])
        upper_range_hz = cast(float, description["upper_range_hz"])
        if frequency >= lower_range_hz and frequency < upper_range_hz:
            return description

    return None


def frequency_description(frequency: float) -> Optional[str]:
    classification = frequency_classification(frequency)

    if classification is None:
        return None

    return classification["description"]


def frequency_caution(frequency: float) -> Optional[str]:
    classification = frequency_classification(frequency)

    if classification is None:
        return None

    return classification["caution"]


def frequency_octave(frequency: float) -> Optional[int]:
    classification = frequency_classification(frequency)

    if classification is None:
        return None

    return classification["octave"]
