from booleval import operators as ops
from booleval.expression import Expression


def test_and_gt_eq_false():
    expr = Expression(ops.And(ops.Gt(5, 6), ops.Eq("5", "5")))
    assert not expr, expr.false
    assert repr(expr.false) == "[<Gt: 5 > 6>]"
