from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Any, Optional, Set, Tuple


@dataclass
class Violation:
    code: str
    line: int
    col: int
    description: str
    filename: str
    node: ast.AST

    @classmethod
    def build(
        cls,
        filename: str,
        vio_details: Tuple[str, str],
        node: ast.AST,
        *args: Any,  # noqa: ANN401
        **kwargs: Any,  # noqa: ANN401
    ) -> Violation:
        code, msg = vio_details
        return cls(code, node.lineno, node.col_offset, msg, filename, node)


@dataclass
class VerboseReraiseViolation(Violation):
    exception_name: str

    @classmethod
    def build(
        cls,
        filename: str,
        vio_details: Tuple[str, str],
        node: ast.AST,
        exception_name: str = "",
        *args: Any,  # noqa: ANN401
        **kwargs: Any,  # noqa: ANN401
    ) -> VerboseReraiseViolation:
        code, msg = vio_details
        return cls(code, node.lineno, node.col_offset, msg, filename, node, exception_name)


@dataclass
class RaiseWithoutCauseViolation(Violation):
    except_node: ast.ExceptHandler
    exception_name: Optional[str] = None

    @classmethod
    def build(
        cls,
        filename: str,
        vio_details: Tuple[str, str],
        node: ast.AST,
        except_node: Optional[ast.ExceptHandler] = None,
        exception_name: Optional[str] = None,
        *args: Any,  # noqa: ANN401
        **kwargs: Any,  # noqa: ANN401
    ) -> RaiseWithoutCauseViolation:
        if except_node is None:
            raise ValueError("except_node")

        code, msg = vio_details
        return cls(
            code, node.lineno, node.col_offset, msg, filename, node, except_node, exception_name
        )


@dataclass
class InheritFromNonBaseViolation(Violation):
    @classmethod
    def build(
        cls,
        filename: str,
        vio_details: Tuple[str, str],
        node: ast.AST,
        class_name: Optional[str] = None,
        allowed_bases: Optional[Set[str]] = None,
        *args: Any,  # noqa: ANN401
        **kwargs: Any,  # noqa: ANN401
    ) -> InheritFromNonBaseViolation:
        code, msg_base = vio_details

        allowed_msg = ", ".join(allowed_bases or set())
        msg = msg_base.format(class_name or "", allowed_msg)

        return cls(code, node.lineno, node.col_offset, msg, filename, node)
