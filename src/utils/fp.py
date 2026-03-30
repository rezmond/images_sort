from functools import reduce


def compose2(f, g):
    return lambda *a, **kw: f(g(*a, **kw))


class Pipe:
    """A class that allows function composition using the | operator.

    Example usage:
        def add_one(x):
            return x + 1

        def multiply_by_two(x):
            return x * 2

        # Create a pipeline and use it
        pipe = Pipe() | add_one | multiply_by_two
        result = pipe(3)  # Returns 8 (3 + 1 = 4, then 4 * 2 = 8)
    """

    fs = []

    def __or__(self, other):
        self.fs.append(other)
        return self

    def __call__(self, x):
        return reduce(lambda acc, f: f(acc), self.fs, x)


def pipe(*functions):
    """Is accepts  several functions as positional arguments for cmpatibilty reasons..

    The actual preferred approach is to use the | operator directly:
        pipe() | func1 | func2
    """
    p = Pipe()
    for f in functions:
        p = p | f
    return p
