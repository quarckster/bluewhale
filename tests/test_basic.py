from bluewhale import operators as ops
from bluewhale.expression import Expression


def test_all_gt_eq_false():
    expr = Expression(ops.All(ops.Gt(5, 6), ops.Eq("5", "5")))
    assert not expr, str(expr)
    assert repr(expr.false) == "[<Gt: 5 > 6>]"


def test_not_all_gt_eq_is_false():
    expr = Expression(ops.Not(ops.All(ops.Gt(7, 6), ops.Eq("5", "5"), ops.Is(True, True))))
    assert not expr, str(expr)
    assert repr(expr.false) == "[<Not: <All: <Gt: 7 > 6>, <Eq: '5' == '5'>, <Is: True is True>>>]"


def test_truth_not_truth_contains():
    expr = Expression(ops.Truth(ops.Not(ops.Truth(ops.Contains("str", "s")))))
    assert not expr, str(expr)
    assert (
        repr(expr.false) == "[<Not: <Truth: <Contains: 's' in 'str'>>>,"
        " <Truth: <Not: <Truth: <Contains: 's' in 'str'>>>>]"
    )
