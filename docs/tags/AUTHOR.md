# @author

## Table of Contents

- [Overview](#overview)
- [Examples](#examples)
- [Related](#related)

## Overview

The `@author` tag attaches a description to a parameter name. When combined with the function or class parsers (future capability), it associates this description with the named parameters.

Parameter data type is acquired from the function or class argument specification.

## Examples

A single author, no email:

```python
def my_function() -> None:
    """
        @author John Doe
    """
```

A single author, with email:

```python
def my_function() -> None:
    """
        @author John Doe [john.doe@somedomain.com]
    """
```

Multiple authors, mixed format
```python
def my_function() -> None:
    """
        @author John Doe [john.doe@somedomain.com]
        @author Frank Dorman [frank.dorman@somedomain.com]
        @author Jane M. Doe
        @author Hannah Marie Smith III [hannahsmith@somedomain.com]
    """
```

## Related

- `@copyright`
- `@license`