from src.util.crypto import get_file_sha256


class Track:
    def __init__(self, file_location: str):
        self.file_location = file_location
        self.sha256 = get_file_sha256(file_location)

    def get_hash(self) -> str:
        return self.sha256
