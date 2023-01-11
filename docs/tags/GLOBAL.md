# @global

## Table of Contents

- [Overview](#overview)
- [Examples](#examples)
- [Related](#related)

## Overview

If marked with a `@global` tag, whatever owns that docstring should get included in the Globals section of the documentation. This is useful for tags that are created locally and then assigned to the Global scope.

This flag defaults to `False`.

## Examples

Using the `@global` tag within the docstring.

```python
def sayHello(name: str, age: int) -> str:
    """
        @global
    """
    return ("Hello, " + name + ", I am " + str(age) + " years old.")
```

## Related

- [`@memberof`](./MEMBEROF.md)
- [`@namespace`](./NAMESPACE.md)
