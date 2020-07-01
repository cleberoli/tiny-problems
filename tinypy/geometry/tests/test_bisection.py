from tinypy.geometry.bisection import Bisection


def test_bisection():
    bisection = Bisection([2, 1], [3, 4])

    assert bisection.left == [1, 2]
    assert bisection.right == [3, 4]


def test_add():
    bisection = Bisection()

    assert bisection.left == []
    assert bisection.right == []

    bisection.add_left(2)
    bisection.add_left(1)
    assert bisection.left == [1, 2]

    bisection.add_right(3)
    bisection.add_right(4)
    assert bisection.right == [3, 4]


def test_str():
    bisection = Bisection([2, 1], [3, 4])

    assert str(bisection) == "{'left': [1, 2], 'right': [3, 4]}"


def test_repr():
    bisection = Bisection([2, 1], [3, 4])

    assert repr(bisection) == '([1, 2], [3, 4])'
