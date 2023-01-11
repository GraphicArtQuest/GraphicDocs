# @since

## Table of Contents

- [Overview](#overview)
- [Examples](#examples)
- [Related](#related)

## Overview

The `@since` tag in the docstring marks that object was included in a particular version.

If more than one `@since` tag is used, only the last one in the docstring will get recorded.

## Examples

A deprecated function.

```python
def sayHello(name: str, age: int) -> str:
    """
        @param name This is the name of the person you are trying to talk to
        @param age This is your current age
        @returns A simple string saying hi to your friend, and how old you are.
        @since 1.2.0
    """
    return ("Hello, " + name + ", I am " + str(age) + " years old.")
```

A function with a `since` description.

```python
def sayHello(name: str, age: int) -> None:
    """
        @param name This is the name of the person you are trying to talk to.
        If needed, your description can spill over onto a second line, or more if needed.
        @param age This is your current age
        @returns A simple string saying hi to your friend, and how old you are.
        If needed, you can make this as long of a description as you want.
        @since version 1.2.5
    """
    return ("Hello, " + name + ", I am " + str(age) + " years old.")
```

A function with a `@since` tag description overridden by another `@since` tag. In this example, the `since` value will be the string `2.0.0` instead of `release version 1.2.5` because of the later tag.

```python
def sayHello(name: str, age: int) -> None:
    """
        @since release version 1.2.5
        @param name This is the name of the person you are trying to talk to.
        If needed, your description can spill over onto a second line, or more if needed.
        @param age This is your current age
        @returns A simple string saying hi to your friend, and how old you are.
        If needed, you can make this as long of a description as you want.
        @since 2.0.0
    """
    return ("Hello, " + name + ", I am " + str(age) + " years old.")
```

## Related

- [`@deprecated`](./DEPRECATED.md)
- [`@version`](./VERSION.md)
