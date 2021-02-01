from src.interpreter.graph_type import GraphType


class AudioFile(GraphType):
    def __init__(self, file_location):
        self.file_location = file_location
