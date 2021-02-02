from enum import Enum


class GraphElementType(Enum):
    UNKNOWN = 0
    TYPE = 1
    TRANSFORM = 2


class GraphNode:
    element_type = GraphElementType.UNKNOWN

    @property
    def class_name(self):
        return type(self).__name__
