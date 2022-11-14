# @ignore

## Table of Contents

- [Overview](#overview)
- [Examples](#examples)
- [Related](#related)

## Overview

The `@ignore` tag marks a function, class, or module as one that should get excluded from the generated documentaiton, regardless of if it is private or public.

This flag defaults to `False`.

This tag works similarly to the `@private` tag, however if outputting both public and private objects to documentation, this will be ignored.

## Examples

Using the `@ignore` tag within the docstring will cause this otherwise public function to get ignored.

```python
def sayHello(name: str, age: int) -> str:
    """
        @public
        @ignore
    """
    return ("Hello, " + name + ", I am " + str(age) + " years old.")
```

Ignoring a private function will still cause it to get omitted from the generated documentation if outputting both public and private variables.

```python
def _sayHello(name: str, age: int) -> str:
    """
        @private
        @ignore
    """
    return ("Hello, " + name + ", I am " + str(age) + " years old.")
```

## Related

- `@private`
- `@public`