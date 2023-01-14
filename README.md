# GraphicDocs

Code is important, but documentation is critical. Spend more time writing code and less time agonizing over how to document it.

----

<div align="center">

[![Documented with GraphicDocs](https://img.shields.io/badge/Documented%20with-GraphicDocs-841561)](https://github.com/GraphicArtQuest/GraphicDocs)

[![Maintained](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg)](#envelope-contact)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](/../../blob/main/CONTRIBUTING.md#contributing-guide)
[![License](https://img.shields.io/github/license/M-Scott-Lassiter/jest-geojson?color=blue)](https://github.com/M-Scott-Lassiter/jest-geojson/blob/main/LICENSE)

</div>

----

<details open="open">
    <summary><b>Table of Contents</b></summary>

- [About](#about)
- [Documenting Conventions](#documenting-conventions)
    - [Supported Annotation Types](#supported-annotation-types)
    - [Supported Docstring Tags](#supported-docstring-tags)
- [Generating Documentation](#generating-documentation)
    - [Building Documentation Using the Core](#building-documentation-using-the-core)
    - [Using the Documentation Parser Independently](#using-the-documentation-parser-independently)
    - [Templates](#templates)
- [Badge and Use in Github Projects](#badge-and-use-in-github-projects)
- [License and Development](#license-and-development)

</div>

----

# About

This project parses Python modules, classes, and functions to generate well formatted documentation.

It does this by taking advantage of several Python features defined in Python Enhancement Proposals. You do not need in depth knowledge of them to use `GraphicDocs`, but for more information see:

- Style Guide for Python Code ([PEP 8](https://peps.python.org/pep-0008/))
- Docstring Conventions ([PEP 257](https://peps.python.org/pep-0257/))
- Type Hints ([PEP 484](https://peps.python.org/pep-0484/))
- Variable Annotations ([PEP 526](https://peps.python.org/pep-0526/))
- Union Types ([PEP 604](https://peps.python.org/pep-0604/))

 It also defines a parseable [docstring tagging convention](#supported-docstring-tags) (inspired by the [JSDoc](https://github.com/jsdoc/jsdoc#jsdoc) project for annotating Javascript code) to record information Python's built in annotations do not.

Following this convention will take a barebones example like this:

```python
def product_is_positive(input1, input2=0):

    result = input1 * input2
    if result > 0:
        return True
    else:
        return False
```

And turn it into a much more understandable example like this:

```python
def product_is_positive(input1: int, input2: float|int = 0) -> bool:
    """ Check if the product of two numbers is positive or not.

        @param input1 The first number.
        @param input2 The second number.
        @returns `True` if input1 and input2 multiplied together are greater than 0,
        `False` otherwise or if input2 is omitted.
        @throws [TypeError] If either `input1` or `input2` are not numbers.
    """

    result = input1 * input2
    if result > 0:
        return True
    else:
        return False
```

Nothing functionally changed between the examples above, but using type hint annotations and the docstring tags made it immediately clearer about what the function does, and more importantly *why*. 

To see some examples of what `GraphicDocs` can create, see its own API documentation it created on itself:

- [`Core`](./docs/api/core.md)
- [`Hooks`](./docs/api/hooks.md)
- [`Parser`](./docs/api/parser.md)

# Documenting Conventions

Python is a dynamically typed language. This means nothing in the Python compiler will prevent you from abusing data types defined through annotations.

## Supported Annotation Types

`GraphicDocs` recognizes and supports the following annotation types for argument and return types:

- `any`
- `bytes`
- `callable`
- `dict`
- `int`
- `False`
- `float`
- `list`
- `None`
- `set`
- `str`
- `True`
- `tuple`

Beyond these, Python allows other entries for annotations. `GraphicDocs` should also work in most cases with:

- Any reference to a module (e.g. `enum`), class (e.g. `enum.Enum`), or function (e.g. `enum.unique`), either built on or custom made
- Any number (e.g. `0`, `101`, `-10`)

You can union these together with the pipe (`|`) character with no limitations on what kind of types you can combine:

```python
def myfunc(input: str|int|None|callable):
    ...
```

## Supported Docstring Tags

`GraphicDocs` provides multiple tags that let you document things Python's annotations do not. At this time, it does not recognize foreign tags (i.e. tags not defined below).

- [@author](./docs/tags/AUTHOR.md)
- [@copyright](./docs/tags/COPYRIGHT.md)
- [@deprecated](./docs/tags/DEPRECATED.md)
- [@example](./docs/tags/EXAMPLE.md)
- [@global](./docs/tags/GLOBAL.md)
- [@ignore](./docs/tags/IGNORE.md)
- [@license](./docs/tags/LICENSE.md)
- [@memberof](./docs/tags/MEMBEROF.md)
- [@namespace](./docs/tags/NAMESPACE.md)
- [@param](./docs/tags/PARAM.md)
- [@private](./docs/tags/PRIVATE.md)
- [@public](./docs/tags/PUBLIC.md)
- [@returns](./docs/tags/RETURNS.md)
- [@since](./docs/tags/SINCE.md)
- [@throws](./docs/tags/THROWS.md)
- [@todo](./docs/tags/TODO.md)
- [@version](./docs/tags/VERSION.md)

Within the docstring, `GraphicDocs` records everything before the first tag as the description. Any carriage returns will get treated as a continuation of the same paragraph. It interprets blank lines as a new paragraph. For example:

```python
def test_function() -> None:
    """ This is the first line in the first paragraph.
        This line continues as the second sentence.

        This line begins a new paragraph.
        @returns Nothing gets returned, and this line ends the description.
    """
```

# Generating Documentation

Download the project `src` folder and import the tool.

This project is not currently available by PIP.  ***COMING SOON!***

## Building Documentation Using the Core

First, build a documentation generating script:

```python
# docs.py

from graphicdocs import Core

config = {
    "source": "./path/to/your/source.py"
}
core = Core(config)

core.build()
```

Then running
```python
python docs.py
```

will output a file `source.md` to the working directory.

## Using the Documentation Parser Independently

You can use the individual parsing functions to get the raw dictionary object:

```python
from graphicdocs import parse_module, parse_class, parse_function, parse_docstring

class my_class():
    ...

my_parsed_class = parse_class(my_class)
```

## Templates

`GraphicDocs` has the following template built in and available.

- [`Graphic_MD`](./docs/templates/graphic_md.md)

You can [make your own templates](https://github.com/GraphicArtQuest/GraphicDocs/blob/main/docs/core.md#templates) that take the parsed data and output into whatever Markdown, HTML, or other output format you want. You can write your template locally, or build and distribute it with PIP.

# Badge and Use in Github Projects

I encourage you to apply the [`graphicdocs`](https://github.com/topics/graphicdocs) Github repository tag if you use this tool so others can see examples in action. Additionally, feel free to add the following badge to your repository:

[![Documented with GraphicDocs](https://img.shields.io/badge/Documented%20with-GraphicDocs-841561)](https://github.com/GraphicArtQuest/GraphicDocs)

    
    [![Documented with GraphicDocs](https://img.shields.io/badge/Documented%20with-GraphicDocs-841561)](https://github.com/GraphicArtQuest/GraphicDocs)

# License and Development

To help as many developers as possible, this project and all other files in this repository are distributed as free and open-source software under the [MIT license][license], © 2022-2023.

Both [contributions](CONTRIBUTING.md) and [bug reports][bugs] welcome.

This add-on is maintained and supported. Submit a [bug report][bugs] if you encounter errors.

Maintained by [M. Scott Lassiter][maintainer].

[license]: LICENSE
[bugs]: https://github.com/GraphicArtQuest/Blender-Scripting-Assistant/issues/new/choose
[maintainer]: https://graphicartquest.com/author/scott-lassiter/
