import ast
from typing import Any, Type

from .base import Specification, SpecificationResultType


class HasAtLeastChild(Specification):
    def __init__(self, child_type: Type[ast.stmt], min: int = 1):
        self.child_type = child_type
        self.min = min

    def _calculate_result(self, candidate: ast.stmt) -> SpecificationResultType:
        children = [
            child for child in ast.iter_child_nodes(candidate) if isinstance(child, self.child_type)
        ]

        if len(children) >= self.min:
            return (True, children)

        return (False, None)


class NodeHasAttr(Specification):
    def __init__(self, attr_name: str, attr_type: Type[ast.expr]):
        self.attr_name = attr_name
        self.attr_type = attr_type

    def _calculate_result(self, candidate: ast.stmt) -> SpecificationResultType:
        if attr := getattr(candidate, self.attr_name, False):
            if isinstance(attr, self.attr_type):
                return True, attr

        return False, None


class NodeHasPropEquals(Specification):
    def __init__(self, attr_name: str, attr_val: Any):
        self.attr_name = attr_name
        self.attr_val = attr_val

    def _calculate_result(self, candidate: ast.stmt) -> SpecificationResultType:
        if attr := getattr(candidate, self.attr_name, False):
            if attr == self.attr_val:
                return True, attr

        return False, None


class NodeHasPropNone(Specification):
    def __init__(self, attr_name: str):
        self.attr_name = attr_name

    def _calculate_result(self, candidate: ast.stmt) -> SpecificationResultType:
        attr = getattr(candidate, self.attr_name, False)
        if attr is None:
            return True, attr

        return False, None


class NodeFirstChildIs(Specification):
    def __init__(self, attr_type: Any, attr_name: str):
        self.attr_name = attr_name
        self.attr_type = attr_type

    def _calculate_result(self, candidate: ast.stmt) -> SpecificationResultType:
        if attr := getattr(candidate, self.attr_name, False):
            if len(attr) > 0:
                first, *_ = attr
                if isinstance(first, self.attr_type):
                    return True, first

        return False, None


class ChildrenAre(Specification):
    def __init__(self, attr_type: Any):
        self.attr_type = attr_type

    def _calculate_result(self, candidate: ast.stmt) -> SpecificationResultType:
        children = [
            child for child in ast.iter_child_nodes(candidate) if isinstance(child, self.attr_type)
        ]

        if children:
            return True, children

        return False, None


class ChildrenFilter(Specification):
    def __init__(self, *specifications):
        self.specifications = specifications

    def _calculate_result(self, candidates) -> SpecificationResultType:
        result = []
        for candidate in candidates:
            if all(
                [specification.is_satisfied_by(candidate) for specification in self.specifications]
            ):
                result.append(candidate)

        if result:
            return True, result

        return False, None
