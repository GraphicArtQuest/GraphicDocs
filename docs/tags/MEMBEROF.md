# @memberof

## Table of Contents

- [Overview](#overview)
- [Examples](#examples)
- [Related](#related)

## Overview

The `@memberof` tag indicates that an object belongs to a namespace or module, even if that is not where the parser ultimately found it. This helps organize your project's documentation.

This is especially useful when encapsulating functions, classes, or variables in other logically separated files. Multiple `@memberof` tags can be used on a single object, and this will cause the object to get duplicate documentation in the final results.

The tag specifies only a name that meets valid Python naming criteria.

If the tags are omitted or included but left blank, it will return `None`. Otherwise, it returns a list of string names.

## Examples

`@memberof` tag defined in a file docstring:

```python
"""
    This is a file docstring.
    It describes what it does

    @memberof Tools
"""

def my_function() -> None:
```

Multiple `@memberof` tags:


```python
"""
    This is a file docstring.
    It describes what it does

    @memberof Tools
    @memberof Workers
    @memberof Construction.Sites
"""
```

## Related

- `@global`
- `@namepsace`
