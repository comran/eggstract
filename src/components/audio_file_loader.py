import numpy as np

from src.components.audio_file import AudioFile
from src.components.wave import Wave
from src.interpreter.graph_transform import GraphTransform


class AudioFileLoader(GraphTransform):
    output_type = Wave
    dependencies = [AudioFile]

    def parse(self, audio_file: AudioFile):
        assert type(audio_file).__name__ == "AudioFile"
        return Wave(np.array([]), 1)
