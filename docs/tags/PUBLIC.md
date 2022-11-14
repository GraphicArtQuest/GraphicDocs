# @public

## Table of Contents

- [Overview](#overview)
- [Examples](#examples)
- [Related](#related)

## Overview

The `@public` tag marks a function, class, or module as public. By default, these objects are treated as public and will normally show up in the generated documentation. You may still use this tag to be explicitly clear to others that you intended to make this object public.

This tag is useful to force a function, class, module, or variable with a that begins with an underscore (`_`), which would normally get treated as private, to be shown in the documentation.

If both a `@public` and `@private` tag is included, then the `@private` tag takes precedence.

## Examples

Using the `@public` tag within the docstring. It is not actually necessary in this case, because this would normally get treated as public.

```python
def sayHello(name: str, age: int) -> str:
    """
        @public
        @param name This is the name of the person you are trying to talk to
        @param age This is your current age
    """
    return ("Hello, " + name + ", I am " + str(age) + " years old.")
```

Beginning the function name with an underscore indicates it is normally private. The `@public` tag is specifically required in this case to make it public.

```python
def _sayHello(name: str, age: int) -> str:
    """
        @public
        @param name This is the name of the person you are trying to talk to
        @param age This is your current age
    """
    return ("Hello, " + name + ", I am " + str(age) + " years old.")
```

This will get treated as private, because the `@private` tag has precedence over `@public`.

```python
def sayHello(name: str, age: int) -> str:
    """
        @private
        @public
        @param name This is the name of the person you are trying to talk to
        @param age This is your current age
    """
    return ("Hello, " + name + ", I am " + str(age) + " years old.")
```

## Related

- `@private`