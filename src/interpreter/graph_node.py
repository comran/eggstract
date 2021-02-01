from enum import Enum


class GraphElementType(Enum):
    TYPE = 1
    TRANSFORM = 2


class GraphNode:
    @property
    def class_name(self):
        return type(self).__name__
