from src.interpreter.graph import GraphException
from src.interpreter.graph_node import GraphElementType, GraphNode


class GraphTransform(GraphNode):
    element_type = GraphElementType.TRANSFORM
    output_type = None
    dependencies = []

    @classmethod
    def verify_dependencies_exist(obj, graph):
        output_type_name = obj.output_type.__name__
        output_node = graph.fetch_node(output_type_name)

        if output_node is None:
            raise GraphException(
                f"Output type [{obj.output_type}] must be defined before creating transform "
                f"[{obj.__name__}]"
            )

        for dependency in obj.dependencies:
            dependency_name = dependency.__name__
            dependency_node = graph.fetch_node(dependency_name)

            if dependency_node is None:
                raise GraphException(
                    f"Dependency [{dependency}] must be defined before creating transform "
                    f"[{obj.__name__}]"
                )
