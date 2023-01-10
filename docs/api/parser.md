# Module: _`parser`_

_Source: [parser.py](../../src/parser.py)_


Table of Contents

- [Imports](#imports)
- [Functions](#functions)
    - [parse_class](#parse_class)
    - [parse_docstring](#parse_docstring)
    - [parse_function](#parse_function)
    - [parse_module](#parse_module)

## Imports

*Modules*
- inspect
- os
- parse_docstring_functions

*Classes*
- Enum (from `enum`)

----

# Functions

## `parse_class`( **`class_ref`** )<a id='parse_class'></a>



|Argument |Type |Default | Description
|:---|:---:|:---|:---|
|`class_ref` |`None` | | |



> Inspect a class and return a dictionary of documentation values.

_Source: [parser.py, lines 142 thru 284](../../src/parser.py)_

**Returns** -> `dict`: a dictionary of documentation values: { annotations: List of tuples as (name: `str`, type: `object`) (or `None`), arguments: Excluding `self`, list of dictionaries as [default: `any`, name: `str`, required: bool, type: any] (or `None`), docstring: Parsed docstring object (or `None`) methods: List of parsed functions (or `None`) name: String of the function name parent: Name of the parent class this class inherited from (or `None`) properties: List of dictionaries for all class properties as [docstring: `dict`, name: `str`, readable: `bool`, writeable: `bool`] }

----

## `parse_docstring`( **`docstring`** )<a id='parse_docstring'></a>



|Argument |Type |Default | Description
|:---|:---:|:---|:---|
|`docstring` |`str` | | |



> Parses a docstring and returns a dict of the string formatted into component parts.
>
> The description must be at the top. Everything before the first tag gets treated as description.
>
> The parser treats consecutive lines as part of a single paragraph. To make a new paragraph, add an additional blank line to separate it from the previous one.
>
> You can use ordered lists by putting them on their own line using either a "-" or "<ul>" character. Omitting the space after the '-' character will not treat it as an unordered list.
>
> Ordered lists can be created with the "<ol>" character before it.
>
> Available Tags:
>
> - @author
>
> - @copyright
>
> - @deprecated
>
> - @example
>
> - @global
>
> - @ignore
>
> - @license
>
> - @memberof
>
> - @namespace
>
> - @param
>
> - @private
>
> - @public
>
> - @returns
>
> - @since
>
> - @throws
>
> - @todo
>
> - @version

_Source: [parser.py, lines 7 thru 66](../../src/parser.py)_

----

## `parse_function`( **`function_ref`** )<a id='parse_function'></a>



|Argument |Type |Default | Description
|:---|:---:|:---|:---|
|`function_ref` |`object` | | |



> Inpsect a function and return a dictionary of documentation values.

_Source: [parser.py, lines 68 thru 140](../../src/parser.py)_

**Returns** -> `dict`: If not passed a function, returns `None`. Otherwise, it returns a dictionary of documentation values for that function:
{ arguments: List of dictionaries as [default: `any`, name: `str`, required: bool, type: any] (or `None`), docstring: Parsed docstring object (or `None`) lineno: Lines in the source code where this occers: tuple(startingline: int, endingline: int) name: String of the function name returns: Whatever the return value type is sourcefile: A string filepath for where this sourcefile is located }

----

## `parse_module`( **`module_ref`** )<a id='parse_module'></a>



|Argument |Type |Default | Description
|:---|:---:|:---|:---|
|`module_ref` |`None` | | |



> This function parses Python module files (i.e. `*.py`).
>
> Functions and classes will always show up in alphabetical order, NOT the order they appear in the file.

_Source: [parser.py, lines 286 thru 348](../../src/parser.py)_

----

Visit [Graphic Art Quest](https://www.GraphicArtQuest.com) for more!