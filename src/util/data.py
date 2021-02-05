import os
import shutil

from src.util import constants
from src.util.crypto import get_file_sha256


def import_track(file_location: str):
    sha256 = get_file_sha256(file_location)
    _, extension = os.path.splitext(file_location)

    file_destination = f"{constants.LIBRARY_AUDIO_ROOT}/{sha256}{extension}"

    print(f"Copying {file_location} -> {file_destination}")
    shutil.copy(file_location, file_destination)

    return sha256
