# @param

## Table of Contents

- [Overview](#overview)
- [Examples](#examples)

## Overview

The `@param` tag attaches a description to a parameter name. When combined with the function or class parsers (future capability), it associates this description with the named parameters.

Parameter data type is acquired from the function or class argument specification.

## Examples

```python
def sayHello(name: str, age: int) -> None:
    """
        @param name This is the name of the person you are trying to talk to
        @param age This is your current age
    """
    return ("Hello, " + name + ", I am " + str(age) + " years old.")
```

```python
def sayHello(name: str, age: int) -> None:
    """
        @param name This is the name of the person you are trying to talk to.
        If needed, your description can spill over onto a second line, or more if needed.
        
        @param age This is your current age
    """
    return ("Hello, " + name + ", I am " + str(age) + " years old.")
```