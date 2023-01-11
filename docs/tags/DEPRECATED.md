# @deprecated

## Table of Contents

- [Overview](#overview)
- [Examples](#examples)
- [Related](#related)

## Overview

The `@deprecated` tag in the docstring marks that object as having been deprecated. You can include text following the tag to describe more about the deprecation.

If more than one `@deprecated` tag is used, only the last one in the docstring will get recorded.

## Examples

A deprecated function.

```python
def sayHello(name: str, age: int) -> str:
    """
        @param name This is the name of the person you are trying to talk to
        @param age This is your current age
        @returns A simple string saying hi to your friend, and how old you are.
        @deprecated
    """
    return ("Hello, " + name + ", I am " + str(age) + " years old.")
```

A deprecated function with a description.

```python
def sayHello(name: str, age: int) -> None:
    """
        @param name This is the name of the person you are trying to talk to.
        If needed, your description can spill over onto a second line, or more if needed.
        @param age This is your current age
        @returns A simple string saying hi to your friend, and how old you are.
        If needed, you can make this as long of a description as you want.
        @deprecated since version 1.2.5
    """
    return ("Hello, " + name + ", I am " + str(age) + " years old.")
```

A deprecated function with a description overridden by another `@deprecated` tag. In this example, the `deprecated` value will be 2.0.0 instead of 1.2.5 because of the later tag.

```python
def sayHello(name: str, age: int) -> None:
    """
        @deprecated since version 1.2.5
        @param name This is the name of the person you are trying to talk to.
        If needed, your description can spill over onto a second line, or more if needed.
        @param age This is your current age
        @returns A simple string saying hi to your friend, and how old you are.
        If needed, you can make this as long of a description as you want.
        @deprecated since version 2.0.0
    """
    return ("Hello, " + name + ", I am " + str(age) + " years old.")
```

## Related

- [`@since`](./SINCE.md)
- [`@version`](./VERSION.md)
