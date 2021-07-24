import operator
from typing import Any
from typing import Callable
from typing import TYPE_CHECKING
from typing import Union

if TYPE_CHECKING:
    from booleval.expression import Expression


class Operator:
    op: Callable
    op_str: str

    def __init__(self, lobj: Union["Operator", Any], robj: Union["Operator", Any]) -> None:
        self._parent: Union["Expression", "Operator"]
        self.lobj = lobj
        self.robj = robj
        self.pure = not isinstance(self.lobj, Operator) and not isinstance(self.robj, Operator)

    @property
    def parent(self) -> Union["Expression", "Operator"]:
        return self._parent

    @parent.setter
    def parent(self, parent: Union["Expression", "Operator"]) -> None:
        self._parent = parent
        if isinstance(self.lobj, Operator):
            self.lobj.parent = self
        if isinstance(self.robj, Operator):
            self.robj.parent = self

    @property
    def expression(self) -> "Expression":
        return getattr(self.parent, "parent", self.parent)

    def __bool__(self) -> bool:
        if isinstance(self.lobj, Operator) and isinstance(self.robj, Operator):
            result = self.op(bool(self.lobj), bool(self.robj))
        elif isinstance(self.lobj, Operator) and not isinstance(self.robj, Operator):
            result = self.op(bool(self.lobj), self.robj)
        elif isinstance(self.robj, Operator) and not isinstance(self.lobj, Operator):
            result = self.op(self.lobj, bool(self.robj))
        else:
            result = self.op(self.lobj, self.robj)
        if self.pure:
            self.expression.report[result].append(self)
        return result

    def __str__(self) -> str:
        return self.op_str

    def __repr__(self) -> str:
        return f"<{type(self).__name__}: {repr(self.lobj)} {self} {repr(self.robj)}>"


class And(Operator):
    op = operator.and_
    op_str = "&"


class Or(Operator):
    op = operator.or_
    op_str = "|"


class Not(Operator):
    op = operator.not_
    op_str = "not"


class Lt(Operator):
    op = operator.lt
    op_str = "<"


class Le(Operator):
    op = operator.le
    op_str = "<="


class Eq(Operator):
    op = operator.eq
    op_str = "=="


class Ne(Operator):
    op = operator.ne
    op_str = "!="


class Ge(Operator):
    op = operator.ge
    op_str = ">="


class Gt(Operator):
    op = operator.gt
    op_str = ">"


class Truth(Operator):
    op = operator.truth
    op_str = "bool"


class Is(Operator):
    op = operator.is_
    op_str = "is"


class IsNot(Operator):
    op = operator.is_not
    op_str = "is not"


class Contains(Operator):
    op = operator.contains
    op_str = "in"
