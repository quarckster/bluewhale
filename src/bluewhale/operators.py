import operator
from typing import Any as AnyType
from typing import Callable
from typing import List
from typing import TYPE_CHECKING
from typing import Union

if TYPE_CHECKING:
    from bluewhale.expression import Expression


class Operator:
    op: Callable
    op_str: str

    def __init__(self, *objs) -> None:
        self._parent: Union["Expression", "Operator"]
        self.objs = objs
        self.pure = True
        for obj in self.objs:
            if isinstance(obj, Operator):
                self.pure = False
                break

    @property
    def parent(self) -> Union["Expression", "Operator"]:
        return self._parent

    @parent.setter
    def parent(self, parent: Union["Expression", "Operator"]) -> None:
        self._parent = parent
        for obj in self.objs:
            if isinstance(obj, Operator):
                obj.parent = self

    @property
    def expression(self) -> "Expression":
        return getattr(self.parent, "expression", self.parent)

    def append_report(self, result: bool) -> None:
        if self.pure:
            self.expression.report[result].append(self)

    @property
    def resolved_objs(self):
        rslvd_objs: List[AnyType] = []
        for obj in self.objs:
            if isinstance(obj, Operator):
                rslvd_objs.append(bool(obj))
            else:
                rslvd_objs.append(obj)
        return rslvd_objs

    def __bool__(self) -> bool:
        result = self.op(*self.resolved_objs)
        self.append_report(result)
        return result

    def __str__(self) -> str:
        if len(self.objs) == 1:
            return f"{self.op_str}({str(self.objs[0])})"
        if len(self.objs) == 2:
            return f"{str(self.objs[0])} {self.op_str} {str(self.objs[1])}"
        pretty = ", ".join([str(obj) for obj in self.objs])
        return f"{self.op_str}({pretty})"

    def __repr__(self) -> str:
        if len(self.objs) == 1:
            return f"<{type(self).__name__}: {repr(self.objs[0])}>"
        if len(self.objs) == 2:
            return (
                f"<{type(self).__name__}: {repr(self.objs[0])} {self.op_str} {repr(self.objs[1])}>"
            )
        pretty = ", ".join([repr(obj) for obj in self.objs])
        return f"<{type(self).__name__}: {pretty}>"


class All(Operator):
    op_str = "all"
    op = all

    def __bool__(self) -> bool:
        result = self.op(self.resolved_objs)  # type: ignore
        self.append_report(result)
        return result


class Any(Operator):
    op_str = "any"
    op = any

    def __bool__(self) -> bool:
        result = self.op(self.resolved_objs)  # type: ignore
        self.append_report(result)
        return result


class Not(Operator):
    op = operator.not_
    op_str = "not"

    def append_report(self, result: bool) -> None:
        self.expression.report[result].append(self)


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

    def append_report(self, result: bool) -> None:
        self.expression.report[result].append(self)


class Is(Operator):
    op = operator.is_
    op_str = "is"


class IsNot(Operator):
    op = operator.is_not
    op_str = "is not"


class Contains(Operator):
    op = operator.contains
    op_str = "in"

    def __str__(self) -> str:
        return f"{str(self.objs[1])} {self.op_str} {str(self.objs[0])}"

    def __repr__(self) -> str:
        return f"<{type(self).__name__}: {repr(self.objs[1])} {self.op_str} {repr(self.objs[0])}>"
