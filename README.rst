Skinpy
=========
Basic usage
-----------
.. code-block:: python

    >>> from skinpy import Testable
    >>> Testable("foo").should_equal("foo")
    >>> Testable("foo").should_equal("bar")
    Traceback (most recent call last):
        ...
    AssertionError: foo doesn't equal 'bar'

.. code-block:: python

    >>> Testable({"foo": "bar"})["foo"].should_equal("bar")
    >>> Testable({"foo": "bar"})["foo"].should_equal("foo")
    Traceback (most recent call last):
        ...
    AssertionError: {'foo': 'bar'}['foo']: 'bar' doesn't equal 'foo'


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
    >>> Testable(foo).foo.should_equal("foo")
    Traceback (most recent call last):
        ...
    AssertionError: <Foo()>.foo: 'bar' doesn't equal 'foo'
    >>> Testable(foo).foobar(foo).foo.should_equal("bar")
    >>> Testable(foo).foobar("foobar").should_equal("barfoo")  # doctest: +SKIP
    Traceback (most recent call last):
        ...
    AssertionError: <Foo()>.foobar('foobar'): 'foobar' doesn't equal 'barfoo'
    >>> Testable(foo).foobar(5).should_raise(ValueError)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    AssertionError: foobar doesn't raise <... '...ValueError'>
