from enum import Enum
import os
from typing import Dict, Optional

from src.library.track import Track

class Library:
    def __init__(self):
        """
        Manages audio files used for training and testing, and associated metadata for those files.
        """

        self.tracks: Dict[str] = {}

    def load_from_folder(self, folder_location: str = "data/tracks"):
        print(f"Loading tracks from folder: {folder_location}\n")

        track_files = []

        # Gather all files in folder.
        for root, _, files in os.walk(folder_location):
            for f in files:
                if not f.endswith(".mp3"):
                    continue

                full_path = os.path.join(root, f)
                track_files.append(full_path)

        # Add tracks to the library.
        for track_file in track_files:
            new_track = self.add_track(track_file)

            if new_track is None:
                print(f" -> Could not add {track_file} to library.")
            else:
                print(f" -> Added {track_file} [{new_track.get_hash()[0:10]}] to library.")

    def add_track(self, file_location: str) -> Track:
        """
        Add a track to the library.
        """

        track = Track(file_location)
        track_hash = track.get_hash()

        if track_hash in self.tracks:
            raise Exception(f"SHA256 hashing collision when adding track to library! [{track_hash}]")

        self.tracks[track_hash] = track

        return track

    def query(self,
              identifier: Optional[str] = None,
              start_time_s: Optional[float] = None,
              end_time_s: Optional[float] = None) -> Optional[Track]:

        if identifier is None:
            raise Exception("Must specify at least one query parameter")

        found_track = None

        if identifier is not None:
            if identifier not in self.tracks:
                return None

            found_track = self.tracks[identifier]

        return found_track
