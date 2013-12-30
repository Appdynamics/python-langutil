Language Utility
================

Currently, this utility only outputs equivalent PHP code.

PHP
---

.. code:: python

    import langutil.php

Converting 'scalars'
~~~~~~~~~~~~~~~~~~~~

A scalar in PHP is anything that is not an object (in PHP:
``!is_object(1) === true``).

.. code:: python

    # Booleans
    langutil.php.generate_scalar(True) == 'true'
    langutil.php.generate_scalar(True, True) == 'TRUE'

    # None turns into null
    langutil.php.generate_scalar(None) == 'null'
    langutil.php.generate_scalar(None, True) == 'null'

    # Numbers are untouched
    langutil.php.generate_scalar(1) == '1'
    langutil.php.generate_scalar(2.5) == '2.5'

    # Strings use single quotes unless it is necessary to use double quotes
    # Double quotes are only necessary if the character has any control codes
    langutil.php.generate_scalar('php code!') == ''php code!''
    langutil.php.generate_scalar('this string has\nnew lines') == '"this string has\nnew lines"'

Converting lists, tuples, dictionaries, etc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These types all resolve to the same type in PHP: the 'PHP array'. The
``generate_array()`` function handles recursive structures but may fail
to detect special objects' underlying structure unless they implement
methods like ``__dict__()``.

All strings (including keys for dictionaries) will default to single
quotes unless double quotes are necessary.

The output will use new lines and two-space indents.

.. code:: python

    langutil.php.generate_array([]) == 'array();'
    langutil.php.generate_array(tuple([])) == 'array();'
    langutil.php.generate_array(set(tuple([]))) == 'array();'
    langutil.php.generate_array({}) == 'array();'

List/set/tuple conversion
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    langutil.php.generate_array([
        1,
        2,
    ])

Output:

.. code:: php

    array(
        1,
        2,
    );

Dictionary conversion
^^^^^^^^^^^^^^^^^^^^^

For dictionaries, order of keys is not guaranteed. In PHP, hashes are
ordered.

.. code:: python

    langutil.php.generate_array({
      'special': '\n',
      'special\x05': 'a string',
      'key': 1,
      'list': [1,2,3],
    })

Output:

.. code:: php

    array(
      'key' => 1,
      'list' => array(
        1,
        2,
        3,
      ),
      "special\x05" => 'a string',
      'special' => "\n",
    );

Serialisation
~~~~~~~~~~~~~

Use ``php.serialize(data_arg)`` for serialising data in PHP's special
serialisation format. The module will try to use the module
``phpserialize`` for this first but has a fallback version in pure
Python for simple values (does not handle 'classes', references, or
'objects').

Note that the types ``list``, ``tuple``, ``set``, and ``dict`` become
PHP arrays (the serialisation format requires 'keys' to be created for
lists so these become integers but should be an equivalent
'integer-based array' in PHP (the number keys do *not* become string
keys).

To unserialize, use ``php.unserialize(str_arg)`` which requires the
``phpserialize`` module.
