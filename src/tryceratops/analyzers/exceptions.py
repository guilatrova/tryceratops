import ast


class AnalyzerException(Exception):
    pass


class AnalyzerVisitException(AnalyzerException):
    def __init__(self, node: ast.stmt):
        self.node = node
        super().__init__(
            f"Unexpected error when analyzing '{type(node).__name__}' statement at "
            f"{node.lineno}:{node.col_offset}"
        )
