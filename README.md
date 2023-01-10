# GraphicDocs

Inspired by the [JSDoc](https://github.com/jsdoc/jsdoc#jsdoc) style for annotating Javascript code, this project defines a convention using Python docstrings and annotations to create better documentation for Python modules, classes, and functions. Your Python scripts are parseable so you can write your own formatting code to automatically generate your documentation, or you can use a built in template such as [`Graphic_MD`](./docs/templates/graphic_md.md).

See the [descriptive documentation](./docs/core.md) to learn more details of configuring `GraphicDocs` and guidance on annotating your projects. Several of the source files have their [API documented](./docs/api/) using `GraphicDocs` on itself.

# Getting Started

Download the project `src` folder and import the tool.

This project is not currently available by PIP.

## Building Documentation Using the Core
The simplest way to document:

```python
from graphicdocs import Core

config = {
    "source": "./path/to/your/source.py"
}

core = Core(config) # Parses on initialization

core.build()    # Outputs a file `source.md` in the working directory
```

## How to Use the Documentation Parser Independently

You can use the individual parsing functions to get the raw dictionary object:

```python
from graphicdocs import parse_module, parse_class, parse_function, parse_docstring

class my_class():
    ...

my_parsed_class = parse_class(my_class)
```

# Support Policy

This add-on is maintained and supported. Submit a [bug report][bugs] if you encounter errors.

# License and Development

To help as many developers as possible, this project and all other files in this repository are distributed as free and open-source software under the [MIT license][license], © 2022.

Both [contributions](CONTRIBUTING.md) and [bug reports][bugs] welcome.

# Contact

Maintained by [M. Scott Lassiter][maintainer].

[license]: LICENSE
[bugs]: https://github.com/GraphicArtQuest/Blender-Scripting-Assistant/issues/new/choose
[maintainer]: https://graphicartquest.com/author/scott-lassiter/