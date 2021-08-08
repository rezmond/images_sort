from functools import reduce


def compose2(f, g):
    return lambda *a, **kw: f(g(*a, **kw))


def pipe(*fs):
    return reduce(compose2, reversed(fs))
