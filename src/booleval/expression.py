from typing import Dict
from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from booleval.operators import Operator


class Expression:
    def __init__(self, op: "Operator"):
        self.op = op
        self.op.parent = self
        self.report: Dict[bool, List["Operator"]] = {True: [], False: []}

    @property
    def false(self) -> List["Operator"]:
        return self.report[False]

    @property
    def true(self) -> List["Operator"]:
        return self.report[True]

    def __bool__(self) -> bool:
        return bool(self.op)
