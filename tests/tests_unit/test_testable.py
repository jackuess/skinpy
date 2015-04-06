import collections
import unittest

import mock

from skinpy import Testable


class TestTestableAsProxy(unittest.TestCase):
    def setUp(self):
        self.dct = {"foo": "bar"}
        Foo = collections.namedtuple("Foo", ["bar"])
        self.obj = Foo("foo")

        def foo(a, b):
            return a, b
        self.callable = foo

    def test_value_should_hold_test_subject(self):
        self.assertEqual(Testable("foo").value, "foo")

    def test_string_representation_should_default_to_subject_name(self):
        self.assertEqual(str(Testable(str)), "str")

    def test_string_representation_should_fallback_to_str_value(self):
        self.assertEqual(str(Testable("foo")), repr("foo"))

    def test_string_representation_should_be_overridable(self):
        self.assertEqual(str(Testable("foo", name="bar")), "bar")

    def test_should_proxy_mappings_as_testables(self):
        self.assertTrue(isinstance(Testable(self.dct)["foo"], Testable))

    def test_test_should_proxy_mappings_with_correct_value(self):
        self.assertEqual(Testable(self.dct)["foo"].value, self.dct["foo"])

    def test_should_proxy_mappings_with_name(self):
        self.assertEqual(str(Testable(self.dct)["foo"]), "{}['foo']".format(self.dct))

    def test_should_proxy_attributes(self):
        self.assertTrue(isinstance(Testable(self.obj).bar, Testable))

    def test_test_should_proxy_attributes_with_correct_value(self):
        self.assertEqual(Testable(self.obj).bar.value, self.obj.bar)

    def test_should_proxy_attributes_with_name(self):
        self.assertEqual(str(Testable(self.obj).bar), "{}.bar".format(self.obj))

    def test_should_proxy_callables(self):
        self.assertEqual(Testable(self.callable)("foo", b="bar").value, ("foo", "bar"))

    def test_should_proxy_callables_with_name(self):
        self.assertEqual(
            str(Testable(self.callable)("foo", b="bar")),
            "foo('foo', b='bar')"
        )


class AbsTestTestableAssertions(unittest.TestCase):
    def setUp(self):
        self.assertion_ctx = mock.Mock(
            return_value=mock.Mock(__enter__=mock.Mock(),
                                   __exit__=mock.Mock(return_value=True))
        )

    def assert_exception_raised_in_assertion_ctx(self, expected_exception_type,
                                                 expected_exception_args,
                                                 expected_testable):
        self.assertion_ctx.assert_called_once_with(expected_testable)
        ctx = self.assertion_ctx.return_value
        self.assertEqual(ctx.__exit__.call_count, 1)
        exc_type, exc_value, _ = ctx.__exit__.call_args[0]
        self.assertEqual(exc_type, expected_exception_type)
        self.assertEqual(exc_value.args, expected_exception_args)


class TestShouldEqual(AbsTestTestableAssertions):
    def setUp(self):
        super(TestShouldEqual, self).setUp()
        self.testable = Testable("foo", assertion_ctx=self.assertion_ctx)

    def test_should_return_testable_on_success(self):
        self.assertEqual(self.testable.should_equal("foo"), self.testable)

    def test_should_store_success_messages(self):
        s_testable = str(self.testable)
        self.assertEqual(str((self.testable.should_equal("foo")
                                           .should_equal("foo"))),
                         "{0} equals 'foo'\n{0} equals 'foo'".format(s_testable))

    def test_should_raise_assertion_error_in_assertion_context_on_failure(self):
        self.testable.should_equal("bar")
        self.assert_exception_raised_in_assertion_ctx(
            expected_exception_type=AssertionError,
            expected_exception_args=("{} doesn't equal 'bar'".format(self.testable),),
            expected_testable=self.testable
        )


class TestShouldRaise(AbsTestTestableAssertions):
    def setUp(self):
        super(TestShouldRaise, self).setUp()

        class CustomExc(Exception):
            pass
        self.CustomExc = CustomExc

        def raise_custom_exc():
            if self.CustomExc:
                raise self.CustomExc
        self.raise_custom_exc = raise_custom_exc
        self.testable = Testable(self.raise_custom_exc, assertion_ctx=self.assertion_ctx)()
        self.str_testable = str(self.testable)

    def test_should_return_testable_on_success(self):
        self.assertEqual(
            self.testable.should_raise(self.CustomExc),
            self.testable
        )

    def test_should_store_success_messages(self):
        self.assertEqual(
            str(self.testable.should_raise(self.CustomExc)),
            "{} raises CustomExc".format(self.str_testable)
        )

    def test_should_raise_assertion_error_on_no_exception_raised(self):
        self.CustomExc = None
        self.testable.should_raise(RuntimeError)
        self.assert_exception_raised_in_assertion_ctx(
            expected_exception_type=AssertionError,
            expected_exception_args=("{} doesn't raise RuntimeError".format(self.str_testable),),
            expected_testable=self.testable
        )
