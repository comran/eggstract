from src.components.audio_file import AudioFile
from src.components.audio_file_loader import AudioFileLoader
from src.components.wave import Wave


def setup_eggstract_components(graph):
    # Types
    graph.define_node(AudioFile)
    graph.define_node(Wave)

    # Transforms
    graph.define_node(AudioFileLoader)
