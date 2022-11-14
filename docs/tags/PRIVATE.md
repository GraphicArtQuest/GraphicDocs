# @private

## Table of Contents

- [Overview](#overview)
- [Examples](#examples)

## Overview

The `@private` tag marks a function, class, or module as private. These will not normally show up in the generated documentation.

As an alternative to using this tag, you can begin the function, class, module, or variable name with an underscore (`_`) to indicate it is private.

## Examples

Using the `@private` tag within the docstring.

```python
def sayHello(name: str, age: int) -> str:
    """
        @private
        @param name This is the name of the person you are trying to talk to
        @param age This is your current age
    """
    return ("Hello, " + name + ", I am " + str(age) + " years old.")
```

Beginning the function name with an underscore indicates private as well with no tag needed.

```python
def _sayHello(name: str, age: int) -> str:
    """
        @param name This is the name of the person you are trying to talk to
        @param age This is your current age
    """
    return ("Hello, " + name + ", I am " + str(age) + " years old.")
```