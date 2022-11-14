# @version

## Table of Contents

- [Overview](#overview)
- [Examples](#examples)
- [Related](#related)

## Overview

The `@version` tag in the docstring annotates the particular version of that object.

If more than one `@version` tag is used, only the last one in the docstring will get recorded.

## Examples

A version specified function.

```python
def sayHello(name: str, age: int) -> str:
    """
        @param name This is the name of the person you are trying to talk to
        @param age This is your current age
        @returns A simple string saying hi to your friend, and how old you are.
        @version 1.2.0
    """
    return ("Hello, " + name + ", I am " + str(age) + " years old.")
```

A function with a `@version` tag description overridden by another `@version` tag. In this example, the `version` value will be the string `2.0.0` instead of `release version 1.2.5` because of the later tag.

```python
def sayHello(name: str, age: int) -> None:
    """
        @version release version 1.2.5
        @param name This is the name of the person you are trying to talk to.
        If needed, your description can spill over onto a second line, or more if needed.
        @param age This is your current age
        @returns A simple string saying hi to your friend, and how old you are.
        If needed, you can make this as long of a description as you want.
        @version 2.0.0
    """
    return ("Hello, " + name + ", I am " + str(age) + " years old.")
```

## Related

- `@deprecated`
- `@since`