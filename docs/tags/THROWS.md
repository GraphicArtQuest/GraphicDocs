# @throws

## Table of Contents

- [Overview](#overview)
- [Examples](#examples)

## Overview

The `@throws` tag describes an error type and a description of why the code will throw that error.

The error type does not have to correspond to an error class that already exists in Python.


## Examples

```python
def sayHello(name: str, age: int) -> str:
    """
        @param name This is the name of the person you are trying to talk to
        @param age This is your current age
        @returns A simple string saying hi to your friend, and how old you are.
        @throws This will throw an error if you do not use a string for the `name` value.
    """
    return ("Hello, " + name + ", I am " + str(age) + " years old.")
```

```python
def sayHello(name: str, age: int) -> None:
    """
        @param name This is the name of the person you are trying to talk to.
        If needed, your description can spill over onto a second line, or more if needed.
        @param age This is your current age
        @returns A simple string saying hi to your friend, and how old you are.
        If needed, you can make this as long of a description as you want.
        @throws [AttributeError] This will throw an error if you do not use a string for the `name` value.
        In this example, the error has been given a specific type.
    """
    return ("Hello, " + name + ", I am " + str(age) + " years old.")
```