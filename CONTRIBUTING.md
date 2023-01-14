# Contributing Guide

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

All commits must follow the Graphic Art Quest [Common Commit Guidance][common_committing] including [types](https://github.com/GraphicArtQuest/Common-Commit-Guidance#types) and [scopes](https://github.com/GraphicArtQuest/Common-Commit-Guidance#scopes).

The following custom scopes are allowed:

- Any [docstring tag](https://github.com/GraphicArtQuest/GraphicDocs#supported-docstring-tags) (e.g. `author`, `example`, `param`, `throws`)
- One of the key source files:
    - `core`
    - `hooks`
    - `parser`
- A template:
    - `grahpic_md`

Changes to how tags are parsed from the [docstring functions](./src/parse_docstring_functions/) should use the relevant tag scope. Use `parser` for changes to the parsing engine itself.

[codeofconduct]: https://github.com/GraphicArtQuest/.github/blob/main/CODE_OF_CONDUCT.md
[securitypolicy]: https://github.com/GraphicArtQuest/.github/blob/main/SECURITY.md
[issues]: https://github.com/GraphicArtQuest/GraphicDocs/issues/new/choose
[common_committing]: https://github.com/GraphicArtQuest/Common-Commit-Guidance
