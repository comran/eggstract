

from enum import Enum
from typing import Dict, Optional

from src.library.track import Track

class Library:
    def __init__(self):
        """
        Manages audio files used for training and testing, and associated metadata for those files.
        """

        self.tracks: Dict[str] = {}

    def add_track(self, file_location: str):
        track = Track(file_location)
        track_hash = track.get_hash()

        if track_hash in self.tracks:
            raise Exception(f"SHA256 hashing collision when adding track to library! [{track_hash}]")

        self.tracks[track_hash] = track

    def query(self,
              identifier: Optional[str] = None,
              start_time_s: Optional[float] = None,
              end_time_s: Optional[float] = None) -> Optional[Track]:

        if identifier is None:
            raise Exception("Must specify at least one query parameter")

        if identifier is not None:
            if identifier not in self.tracks:
                return None

            return self.tracks[identifier]
