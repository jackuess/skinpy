Skinpy
=========
Basic usage
-----------
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
