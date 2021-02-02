import pytest

from src.components import audio_file, audio_file_loader, components
from src.interpreter import graph, graph_exception


def test_graph_construction():
    test_graph = graph.Graph()
    components.setup_eggstract_components(test_graph)


def test_define_instantiated_node():
    test_graph = graph.Graph()

    # Classes should not be instantiated when used to define new nodes.
    with pytest.raises(graph_exception.GraphException):
        test_graph.define_node(audio_file.AudioFile("test_file.wav"))


def test_define_node_twice():
    test_graph = graph.Graph()
    test_graph.define_node(audio_file.AudioFile)

    # Defining the same node twice should raise an error.
    with pytest.raises(graph_exception.GraphException):
        test_graph.define_node(audio_file.AudioFile)


def test_define_out_of_order():
    test_graph = graph.Graph()

    with pytest.raises(graph_exception.GraphException):
        test_graph.define_node(audio_file_loader.AudioFileLoader)


def test_parse_yaml_string():
    # Construct the graph.
    test_graph = graph.Graph()
    components.setup_eggstract_components(test_graph)

    # Create a YAML query.
    output = test_graph.query_yaml_string(
        """
Node: AudioFileLoader
Dependencies:
    - Node: AudioFile
      Params:
          file_location: test.wav
"""
    )
    assert type(output).__name__ == "Wave"

    with pytest.raises(KeyError):
        test_graph.query_yaml_string(
            """
Node: AudioFileLoader
"""
        )
