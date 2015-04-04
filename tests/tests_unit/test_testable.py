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

    def test_string_representation_should_default_to_str_value(self):
        self.assertEqual(str(Testable("foo")), "foo")

    def test_string_representation_should_be_overridable(self):
        self.assertEqual(str(Testable("foo", name="bar")), "bar: 'foo'")

    def test_should_proxy_mappings_as_testables(self):
        self.assertTrue(isinstance(Testable(self.dct)["foo"], Testable))

    def test_test_should_proxy_mappings_with_correct_value(self):
        self.assertEqual(Testable(self.dct)["foo"].value, self.dct["foo"])

    def test_should_proxy_mappings_with_name(self):
        self.assertEqual(str(Testable(self.dct)["foo"]), "{}['foo']: 'bar'".format(self.dct))

    def test_should_proxy_attributes(self):
        self.assertTrue(isinstance(Testable(self.obj).bar, Testable))

    def test_test_should_proxy_attributes_with_correct_value(self):
        self.assertEqual(Testable(self.obj).bar.value, self.obj.bar)

    def test_should_proxy_attributes_with_name(self):
        self.assertEqual(str(Testable(self.obj).bar), "{}.bar: {!r}".format(self.obj, self.obj.bar))

    def test_should_proxy_callables(self):
        self.assertEqual(Testable(self.callable)("foo", b="bar").value, ("foo", "bar"))

    def test_should_proxy_callables_with_name(self):
        self.assertEqual(
            str(Testable(self.callable)("foo", b="bar")),
            "foo('foo', b='bar'): ('foo', 'bar')"
        )


class AbsTestTestableAssertions(unittest.TestCase):
    def setUp(self):
        class Assertion(object):
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, traceback):
                self.exc_value = exc_value
                self.exc_type = exc_type
                return True

            success = mock.Mock()
        self.assertion = Assertion()
        testcase = self

        class MockReporter(object):
            def make_assertion(self):
                return testcase.assertion
        self.reporter = MockReporter()
        self.testable = Testable("foo", reporter=self.reporter)


class TestShouldEqual(AbsTestTestableAssertions):
    def test_should_report_success(self):
        self.testable.should_equal("foo")
        self.assertion.success.assert_called_once_with("{} equals 'foo'".format(self.testable))

    def test_should_raise_assertion_error_inside_ctx_manager(self):
        self.testable.should_equal("bar")
        self.assertIs(self.assertion.exc_type, AssertionError)
        self.assertIsInstance(self.assertion.exc_value, AssertionError)

    def test_should_raise_assertion_with_descriptive_message(self):
        self.testable.should_equal("bar")
        self.assertEqual(
            self.assertion.exc_value.args,
            ("{} doesn't equal 'bar'".format(self.testable),)
        )


class TestShouldRaise(AbsTestTestableAssertions):
    def setUp(self):
        super(TestShouldRaise, self).setUp()

        class CustomExc(Exception):
            pass
        self.CustomExc = CustomExc

    def test_should_report_success_if_correct_exception_raised(self):
        def foo():
            raise self.CustomExc
        Testable(foo, reporter=self.reporter)().should_raise(self.CustomExc)
        self.assertion.success.assert_called_once_with(
            "{} raises {!r}".format(self.testable, self.CustomExc)
        )

    def test_should_raise_assertion_error_if_incorrect_exception_raised(self):
        def foo():
            raise RuntimeError
        Testable(foo, reporter=self.reporter).should_raise(self.CustomExc)
        self.assertEqual(
            self.assertion.exc_value.args,
            ("{} doesn't raise {!r}, it raises RuntimeError()".format(
                self.testable,
                self.CustomExc),)
        )

    def test_should_raise_assertion_error_if_no_exception_raised(self):
        def foo():
            pass
        Testable(foo, reporter=self.reporter).should_raise(self.CustomExc)
        self.assertEqual(
            self.assertion.exc_value.args,
            ("{} doesn't raise {!r}".format(
                self.testable,
                self.CustomExc),)
        )
