Skinpy
=========
Writing tests
-------------

.. code-block:: python

    >>> from skinpy import Description, Subject
    >>> from skinpy.reporters import ConsoleReporter
    >>> class StringDescription(Description):
    ...     @Subject
    ...     def str(self):
    ...         return str
    ...
    ...     def describe(self):
    ...       yield self.str("foo").should_equal("foo")
    ...       yield self.str("foo").should_equal("bar")
    ...
    ...       yield self.str("foo").join(["bar", "BAR"]).should_equal("barfooBAR")
    ...       yield self.str(",").join(["bar", "BAR"]).should_equal("barfooBAR")
    ...
    ...       yield self.str("{0:.2f}").format("foo").should_raise(ValueError)
    ...       yield self.str("{0:.2f}").format("foo").should_raise(TypeError)
    ...
    >>> reporter = ConsoleReporter()
    >>> test_result = StringDescription().execute(reporter)  # doctest: +ELLIPSIS
    str
      ✓ str('foo') equals 'foo'
      ✗ str('foo') doesn't equal 'bar'
      ✓ str('foo').join(['bar', 'BAR']) equals 'barfooBAR'
      ✗ str(',').join(['bar', 'BAR']) doesn't equal 'barfooBAR'
      ✓ str('{0:.2f}').format('foo') raises ValueError
      "str('{0:.2f}').format('foo')" raised a ValueError. Traceback:
        ...
      ValueError: ...
    >>> test_result
    <TestResult(successful=3, failed=2, errors=1)

`Description` tests also support fixtures:

.. code-block:: python

    >>> class IntDescription(Description):
    ...     @Subject
    ...     def int(self):
    ...         print("Returning test subject")
    ...         return int
    ...
    ...     @int.before
    ...     def my_fixture(self):
    ...         print("Set up")
    ...
    ...     @my_fixture.set_tear_down
    ...     def my_fixture(self):
    ...         print("Tear down")
    ...
    ...     def describe(self):
    ...         yield self.int(5.5).should_equal(5)
    ...
    >>> test_result += IntDescription().execute(reporter)  # doctest: +ELLIPSIS
    <BLANKLINE>
    int
    Set up
    Returning test subject
    Tear down
      ✓ int(5.5) equals 5
    >>> test_result
    <TestResult(successful=4, failed=2, errors=1)


Testable
--------
`Testable` is the corner stone in Skinpy.

.. code-block:: python

    >>> from skinpy import Testable
    >>> Testable("foo").should_equal("foo")
    <Testable(subject='foo')>
    >>> Testable("foo").should_equal("bar")
    Traceback (most recent call last):
        ...
    AssertionError: 'foo' doesn't equal 'bar'

.. code-block:: python

    >>> Testable({"foo": "bar"})["foo"].should_equal("bar")
    <Testable(subject={'foo': 'bar'}['foo'])>
    >>> Testable({"foo": "bar"})["foo"].should_equal("foo")
    Traceback (most recent call last):
        ...
    AssertionError: {'foo': 'bar'}['foo'] doesn't equal 'foo'


.. code-block:: python

    >>> class Foo(object):
    ...     foo = "bar"
    ...  
    ...     def foobar(self, value):
    ...         return value
    ...
    ...     def __repr__(self):
    ...         return "<Foo()>"
    ...
    >>> foo = Foo()
    >>> Testable(foo).foo.should_equal("bar")
    <Testable(subject=<Foo()>.foo)>
    >>> Testable(foo).foo.should_equal("foo")
    Traceback (most recent call last):
        ...
    AssertionError: <Foo()>.foo doesn't equal 'foo'
    >>> Testable(foo).foobar(foo).foo.should_equal("bar")
    <Testable(subject=<Foo()>.foobar(<Foo()>).foo)>
    >>> Testable(Foo)().foobar("foobar").should_equal("barfoo")
    Traceback (most recent call last):
        ...
    AssertionError: Foo().foobar('foobar') doesn't equal 'barfoo'
    >>> Testable(foo).foobar(5).should_raise(ValueError)
    Traceback (most recent call last):
        ...
    AssertionError: <Foo()>.foobar(5) doesn't raise ValueError
