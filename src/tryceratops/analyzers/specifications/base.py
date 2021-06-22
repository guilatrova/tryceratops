from typing import Any, Tuple

SpecificationResultType = Tuple[bool, Any]


class Specification:
    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __xor__(self, other):
        return Xor(self, other)

    def __invert__(self):
        return Invert(self)

    def _calculate_result(self, candidate) -> SpecificationResultType:
        raise NotImplementedError()

    def is_satisfied_by(self, candidate) -> bool:
        satisfied, result = self._calculate_result(candidate)
        self.result = result
        return satisfied

    def remainder_unsatisfied_by(self, candidate):
        if self.is_satisfied_by(candidate):
            return None
        else:
            return self


class CompositeSpecification(Specification):
    pass


class MultaryCompositeSpecification(CompositeSpecification):
    def __init__(self, *specifications):
        self.specifications = specifications


class And(MultaryCompositeSpecification):
    def __and__(self, other):
        if isinstance(other, And):
            self.specifications += other.specifications
        else:
            self.specifications += (other,)
        return self

    def is_satisfied_by(self, candidate):
        next_candidate = candidate
        for spec in self.specifications:
            if spec.is_satisfied_by(next_candidate):
                next_candidate = spec.result
            else:
                return False

        self.result = next_candidate
        return True

    def remainder_unsatisfied_by(self, candidate):
        non_satisfied = [
            specification
            for specification in self.specifications
            if not specification.is_satisfied_by(candidate)
        ]
        if not non_satisfied:
            return None
        if len(non_satisfied) == 1:
            return non_satisfied[0]
        if len(non_satisfied) == len(self.specifications):
            return self
        return And(*non_satisfied)


class Or(MultaryCompositeSpecification):
    def __or__(self, other):
        if isinstance(other, Or):
            self.specifications += other.specifications
        else:
            self.specifications += (other,)
        return self

    def is_satisfied_by(self, candidate):
        satisfied = any(
            [specification.is_satisfied_by(candidate) for specification in self.specifications]
        )
        return satisfied


class UnaryCompositeSpecification(CompositeSpecification):
    def __init__(self, specification):
        self.specification = specification


class Invert(UnaryCompositeSpecification):
    def is_satisfied_by(self, candidate):
        return not self.specification.is_satisfied_by(candidate)


class BinaryCompositeSpecification(CompositeSpecification):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Xor(BinaryCompositeSpecification):
    def is_satisfied_by(self, candidate):
        return self.left.is_satisfied_by(candidate) ^ self.right.is_satisfied_by(candidate)


class NullaryCompositeSpecification(CompositeSpecification):
    pass


class TrueSpecification(NullaryCompositeSpecification):
    def is_satisfied_by(self, candidate):
        return True


class FalseSpecification(NullaryCompositeSpecification):
    def is_satisfied_by(self, candidate):
        return False
