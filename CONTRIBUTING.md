# Contributing Guide

<div align="center">

[![semantic-release: angular](https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release)](https://github.com/semantic-release/semantic-release)

</div>

**Thank you for contributing to `GraphicDocs`!**

Before contributing, please take a moment to read through this document. This guide documents the standards, tooling, and processes that go into the CI/CD pipeline.

<details open="open">
    <summary><b>Table of Contents</b></summary>

- [Code of Conduct](#code-of-conduct)
-   [How can I Contribute?](#how-can-i-contribute)
    -   [Submit Issues](#submit-issues)
    -   [Propose New Tags](#propose-new-tags)
    -   [Submit a Pull Request](#submit-a-pull-request)
- [Commits](#commits)
- [Development](#development)
    -   [Local Installation](#local-installation)
    -   [Project Structure](#project-structure)
    -   [Testing](#testing)
    -   [API Documentation](#api-documentation)
    -   [Building](#building)

</details>

## Code of Conduct

Please help keep this project open and inclusive. Refer to the Graphic Art Quest [Common Code of Conduct][codeofconduct] before your first contribution.

## How can I Contribute?

### Submit Issues

**Bug Reports**: Be as detailed as possible, and fill out all information requested in the [bug report template][issues].

_For security related issues, see the [security policy][securitypolicy]._

**Documentation Requests**: Is something unclear in the documentation or the API? Submit a [documentation change request][issues]! Be as detailed as possible. If you have the question, chances are someone else will also who isn't as willing to speak up as you are. If you want to do it yourself, see the [documentation guidelines](#documentation) for instructions.

### Propose New Tags

New tag requests are welcome. **Please ask** before embarking on any significant undertaking (e.g. implementing a new tag, major code refactoring), otherwise you risk wasting time on something that might not fit well with the project. Do this by opening an issue for the proposal.

### Submit a Pull Request

Good pull requests are outstanding help. They should remain focused in scope and avoid unrelated commits.

To submit a pull request,

1. Fork and clone the repository
2. Create a branch for your edits
3. Make sure your work follows the [commits](#commits) guidance

## Commits

All commits must follow the Graphic Art Quest [Common Commit Guidance][common_committing] guidelines, types, and scopes.

The following [custom scopes](https://github.com/GraphicArtQuest/Common-Commit-Guidance#scopes) are allowed:

- Any [docstring tag](https://github.com/GraphicArtQuest/GraphicDocs#supported-docstring-tags) (e.g. `author`, `example`, `param`, `throws`)
- One of the key source files:
    - `core`
    - `hooks`
    - `parser`
- A template:
    - `grahpic_md`

Changes to how tags are parsed from the [docstring functions](./src/parse_docstring_functions/) should use the relevant tag scope. Use `parser` for changes to the parsing engine itself.

## Development

This project requires you to have [Python](https://www.python.org/downloads/) installed.

### Local Installation

```bash
git clone https://github.com/GraphicArtQuest/GraphicDocs.git
cd GraphicDocs
```

After installing, you should [run the test script](#testing) to verify everything works without runtime errors before you start modifying.

### Project Structure

```
├── docs
│   ├── api
│   ├── tags
│   ├── templates
|   └── core.md
├── src
│   ├── parse_docstring_functions
│   ├── plugins
│   ├── templates
|   ├── core.py
|   ├── hooks.py
|   └── parser.py
├── tests
|   ├── core
|   └── parser
```

- `docs`: 
    - `api`: Automatically generated with `GraphicDocs` itself; make no changes by hand here
    - `tags`: Detailed examples on use of each docstring tag
    - `templates`: Detailed instructions on how to use the built-in templates
    - `core.md`: Detailed instructions on how to use all the features within the core engine
- `src`: contains all source files
    - `parse_docstring_functions`: individual tag parsing functions, split up for modularity
    - `plugins`: built-in plugins that ship with `GraphicDocs`
    - `templates`: built-in templates that ship with `GraphicDocs`
    - `core.md`: The main code that directs the parsing, organizing, and creation of code documentation
    - `hooks.py`: A system of filters and actions that the core, plugins, and templates use to extend functionality
    - `parser.py`: The engine behind parsing docstrings into a usable dictionary object
- `tests`: The `unittest` scripts used to verify the core, hooks, and parser work as designed

### Testing

This project uses the `unittest` suite. To run all tests, open the console and enter:

```bash
python test.py
```

### API Documentation

Most of the project's documentation is (ironically) created by hand in order to guide users through detailed steps of how to setup and configure the tool. HOWEVER, the API documentation itself gets created by running the following console command:

```bash
python docs.py
```

### Building

There is currently no build step in this project.

[codeofconduct]: https://github.com/GraphicArtQuest/.github/blob/main/CODE_OF_CONDUCT.md
[securitypolicy]: https://github.com/GraphicArtQuest/.github/blob/main/SECURITY.md
[issues]: https://github.com/GraphicArtQuest/GraphicDocs/issues/new/choose
[common_committing]: https://github.com/GraphicArtQuest/Common-Commit-Guidance
