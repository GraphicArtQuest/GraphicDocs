# @license

## Table of Contents

- [Overview](#overview)
- [Examples](#examples)
- [Related](#related)

## Overview

The `@license` tag in the docstring annotates the license associated with that object.

Any text on the same line as `@license` will be recorded as the license name. All text following until the end of the docstring or the next tag is the optional license text.

If more than one `@license` tag is used, only the last one in the docstring will get recorded. Using `@license` with no text will get ignored and return `None`.

## Examples

A `@license` tag that specifies the license by name only.

```python
def my_function() -> None:
    """
        This is a function that does some stuff.
        @license Apache-2.0
    """
```

A function with only the license terms specified.

```python
def my_function() -> None:
    """
        This is a function that does some stuff.
        @license
        This license lets you do stuff. It does not have an existing name.
    """
```

A function with a `@license` that specifies both the name and text. This example uses the MIT license.

```python
def my_function() -> None:
    """
        This is a function that does some stuff.
        
        @license MIT
        Copyright (c) 2022 Example Corporation Inc.
        
        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.
    """
```

## Related

- `@copyright`
