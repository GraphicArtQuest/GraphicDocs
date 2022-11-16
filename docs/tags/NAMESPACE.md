# @namespace

## Table of Contents

- [Overview](#overview)
- [Examples](#examples)
- [Related](#related)

## Overview

The `@namespace` tag indicates that an object creates a namespace for its members to help organize your project's documentation.

The tag must have a name that meets valid Python naming criteria. It may also contain an optional description of the namespace.

If the tags are omitted or included but left blank, it will return `None`.

Because namespaces are distinct entities, it does not matter in which docstring you define them. Therefore, you may define as many namespaces as needed in a docstring.

## Examples

Namespaces defined in a file docstring:

```python
"""
    This is a file docstring.

    @namespace Tools
    @namespace Tools.Hammers
    @namespace WorkVehicles
    This is a description of the WorkVehicles namespace.

    Separate with a blank line to make a new paragraph.

    @namespace _thisavalidname
    @namespace 2invalidname 
"""
# The "2invalidname" namespace will not register because it starts with a number.

def my_function() -> None:
```

Namespaces defined in a function:


```python
def my_function() -> None:
    """
        @namespace Tools.Wrenches
    """
```

## Related

- `@global`
- `@memberof`
