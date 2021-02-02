from typing import Any, List, cast

import yaml

from src.interpreter.graph_exception import GraphException
from src.interpreter.graph_node import GraphElementType, GraphNode
from src.interpreter.graph_transform import GraphTransform


class Graph:
    def __init__(self):
        self.defined_nodes = {}

    def define_node(self, new_node: GraphNode):
        if not isinstance(new_node, type):
            raise GraphException(
                "Must provide an uninstantiated type when defining a new graph node"
            )

        node_class_name = new_node.__name__

        if node_class_name in self.defined_nodes:
            raise GraphException(f"Node [{node_class_name}] was already defined in the graph")

        if new_node.element_type == GraphElementType.TRANSFORM:
            new_transform_node = cast(GraphTransform, new_node)
            new_transform_node.verify_dependencies_exist(self)

        self.defined_nodes[node_class_name] = new_node

    def fetch_node(self, node_name: str):
        if node_name in self.defined_nodes:
            return self.defined_nodes[node_name]

        return None

    def query_yaml_string(self, yaml_data: str):
        query = yaml.load(yaml_data)
        return self.parse(query)

    def parse(self, query: Any):
        assert isinstance(query, dict)
        assert "Node" in query.keys()

        # Verify that type exists, and fetch the corresponding definition.
        allowed_keys = ["Node"]
        node = self.fetch_node(query["Node"])
        assert node is not None

        if node.element_type == GraphElementType.TYPE:
            allowed_keys.append("Params")
            self.check_query_keys(query, allowed_keys)

            params = {}
            if "Params" in query:
                params = query["Params"]

            return node(**params)
        elif node.element_type == GraphElementType.TRANSFORM:
            allowed_keys.append("Dependencies")
            self.check_query_keys(query, allowed_keys)

            query_dependencies = query["Dependencies"]
            assert isinstance(query_dependencies, list)

            parsed_dependencies = []
            for node_dependency, query_dependency in zip(node.dependencies, query_dependencies):
                parsed_dependency = self.parse(query_dependency)
                assert node_dependency.__name__ == type(parsed_dependency).__name__

                parsed_dependencies.append(parsed_dependency)

            output = node().parse(*parsed_dependencies)
            assert type(output).__name__ == node.output_type.__name__

            return output
        else:
            raise GraphException(f"Unknown GraphElementType: [{node.element_type}]")

    def check_query_keys(self, query: dict, allowed_keys: List[str]):
        allowed_keys_set = set(allowed_keys)
        for key in query.keys():
            assert key in allowed_keys_set
