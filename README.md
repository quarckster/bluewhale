# Blue whale

`Blue whale` is a library for evaluation of boolean expressions. It exports a set of classes
corresponding to the intrinsic operators of Python which return a boolean value.

## Intention

In the most of the cases Python intrinsic operators is enough to use for evaluation:

```python

def test(some_obj_1, some_obj_2) -> bool:
    return some_obj_1.int_prop > some_obj_2.int_prop and some_obj_1.str_prop == some_obj_2.str_prop
```

The problem of the example is that if `test()` returns `False` it's unknown which of the expressions
are `False`. Using `Blue whale` you can rewrite the example in the following way:

```python
from bluewhale import operators as ops
from bluewhale.expression import Expression

def test(some_obj_1, some_obj_2) -> Expression:
    return Expression(ops.All(
        ops.Gt(some_obj_1.int_prop, some_obj_2.int_prop),
        ops.Eq(some_obj_1.str_prop, some_obj_2.str_prop)
    ))

expr = test()
```

If `expr == False` then you can examine `expr.false` to find out which exact expressions are failed.
