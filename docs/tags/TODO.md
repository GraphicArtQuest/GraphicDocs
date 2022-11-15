# @todo

## Table of Contents

- [Overview](#overview)
- [Examples](#examples)

## Overview

The `@todo` tag provides a way to mark something to be completed later. You can use an unlimited number of these tags in the docstring.

If the tags are omitted or included but left blank, it will return `None`.

## Examples

A single `todo`:

```python
def my_function() -> None:
    """
        This is a function that does some stuff.
        @todo I need to do some stuff still.
    """
```

Multiple `todo` tags:


```python
def my_function() -> None:
    """
        This is a function that does some stuff.
        @todo I need to do some stuff still.
        @todo I need to do some more stuff still.
        @todo How is the stuff not done.
        @todo I think this got away from me.
    """
```
