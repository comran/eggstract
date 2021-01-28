import json
import os
import shutil
from enum import Enum
from typing import Dict, Optional

from src.library.track import Track

LIBRARY_FOLDER = "data/raw/library"
LIBRARY_AUDIO_FOLDER = f"{LIBRARY_FOLDER}/audio"
LIBRARY_METADATA_FOLDER = f"{LIBRARY_FOLDER}/metadata"
LIBRARY_METADATA_FILE = f"{LIBRARY_METADATA_FOLDER}/metadata.json"


class Library:
    def __init__(self):
        """
        Manages audio files used for training and testing, and associated metadata for those files.
        """

        # Create directories in raw.
        os.makedirs(LIBRARY_AUDIO_FOLDER, exist_ok=True)
        os.makedirs(LIBRARY_METADATA_FOLDER, exist_ok=True)

        # Fetch or create metadata dictionary.
        if os.path.isfile(LIBRARY_METADATA_FILE):
            with open(LIBRARY_METADATA_FILE) as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {"tracks": []}

        # Create structure for storing the actual Track objects.
        self.tracks: Dict[str] = {}

    def flush_metadata_to_file(self):
        with open(LIBRARY_METADATA_FILE, "w") as f:
            json.dump(self.metadata, f)

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

        if track_hash in self.metadata["tracks"]:
            print(f"Track [{track_hash[0:10]}] already exists in the library!")
            return track

        _, file_extension = os.path.splitext(file_location)
        if file_extension[1:] != "mp3":
            raise NotImplementedError("Currently cannot handle audio files other than mp3")

        self.metadata["tracks"].append(track_hash)

        shutil.copy(file_location, f"{LIBRARY_AUDIO_FOLDER}/{track_hash}{file_extension}")

        self.tracks[track_hash] = track
        self.flush_metadata_to_file()

        return track

    def query(
        self,
        identifier: Optional[str] = None,
        start_time_s: Optional[float] = None,
        end_time_s: Optional[float] = None,
    ) -> Optional[Track]:

        if identifier is None:
            raise Exception("Must specify at least one query parameter")

        found_track = None

        if identifier is not None:
            if identifier not in self.tracks:
                return None

            found_track = self.tracks[identifier]

        return found_track
