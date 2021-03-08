from unittest import TestCase


def assert_dict_equal(*args, **kwargs):
    test_case = TestCase()
    test_case.maxDiff = None
    test_case.assertDictEqual(*args, **kwargs)
