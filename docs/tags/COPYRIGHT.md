# @copyright

## Table of Contents

- [Overview](#overview)
- [Examples](#examples)
- [Related](#related)

## Overview

The `@copyright` tag provides a way to mark copyright information. You can use an unlimited number of these tags in the docstring.

If the tags are omitted or included but left blank, it will return `None`.

## Examples

A single `copyright`:

```python
def my_function() -> None:
    """
        This is a function that does some stuff.
        @copyright I need to do some stuff still.
    """
```

Multiple `copyright` tags:


```python
def my_function() -> None:
    """
        This is a function that does some stuff.

        @copyright Person A, 2010
        @copyright Some Company, 2012
        @copyright Person B, 2017
        @copyright Another Company, 2022
    """
```

## Related

- `@license`
