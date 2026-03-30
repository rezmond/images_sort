from src.utils.fp import pipe


def test_pipe():
    def add_one(x):
        return x + 1

    def multiply_by_two(x):
        return x * 2

    def subtract_five(x):
        return x - 5

    def add_three(x):
        return x + 3

    # Test with a simple function
    f = pipe() | add_one | multiply_by_two
    assert f(3) == 8

    # Test with multiple functions
    f = pipe() | add_one | multiply_by_two | add_one | subtract_five
    assert f(3) == 4

    # Test with no functions
    f = pipe() | add_one | multiply_by_two
    assert f(3) == 8

    # Test with a single function in the pipe
    f = pipe() | multiply_by_two
    assert f(3) == 6

    # Test with chaining multiple pipes
    pipe5 = pipe() | add_three
    assert pipe5(3) == 6


def test_pipe_backward_compatibility():
    def add_one(x):
        return x + 1

    def multiply_by_two(x):
        return x * 2

    # Test pipe function
    f = pipe(add_one, multiply_by_two)
    assert f(3) == 8
