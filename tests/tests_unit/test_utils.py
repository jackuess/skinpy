import unittest

from skinpy.utils import CallProxy


class TestCallProxy(unittest.TestCase):
    def test_registered_object_should_be_intact(self):
        obj = object()
        self.assertIs(CallProxy().register(name="")(obj), obj)

    def test_registered_object_should_be_proxied(self):
        def foo(arg, kwarg):
            return arg, kwarg
        proxy = CallProxy()
        proxy.register("foo")(foo)

        self.assertEqual(proxy("foo", 1, kwarg=2), (1, 2))
