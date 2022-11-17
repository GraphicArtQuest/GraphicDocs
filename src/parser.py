import src.parse_docstring_functions as parse_docstring_functions

def parse_docstring(docstring: str) -> dict:
    """
        Parses a docstring and returns a dict of the string formatted into component parts.
        
        The description must be at the top. Everything before the first tag gets treated as description.

        The parser treats consecutive lines as part of a single paragraph. To make a new paragraph, add an additional
        blank line to separate it from the previous one.

        You can use ordered lists by putting them on their own line using either a "-" or "<ul>" character.
        Omitting the space after the '-' character will not treat it as an unordered list.

        Ordered lists can be created with the "<ol>" character before it.

        Available Tags:

        - @author
        - @copyright
        - @deprecated
        - @example
        - @global
        - @ignore
        - @license
        - @memberof
        - @namespace
        - @param
        - @private
        - @public
        - @returns
        - @since
        - @throws
        - @todo
        - @version
    """

    # Guard clause
    if not isinstance(docstring, str):
        return

    return {
        "description": parse_docstring_functions.get_description(docstring),

        # Tags (Alphabetical Order)
        "author": parse_docstring_functions.get_authors(docstring),
        "copyright": parse_docstring_functions.get_copyright(docstring),
        "deprecated": parse_docstring_functions.get_deprecated(docstring),
        "examples": parse_docstring_functions.get_examples(docstring),
        "global": parse_docstring_functions.get_global(docstring),
        "ignore": parse_docstring_functions.get_ignore(docstring),
        "license": parse_docstring_functions.get_license(docstring),
        "memberof": parse_docstring_functions.get_memberof(docstring),
        "namespaces": parse_docstring_functions.get_namespaces(docstring),
        "parameters": parse_docstring_functions.get_parameters(docstring),
        "private": parse_docstring_functions.get_private(docstring), # If False, this implicitly makes this a public module
        "returns": parse_docstring_functions.get_returns(docstring),
        "since": parse_docstring_functions.get_since(docstring),
        "throws": parse_docstring_functions.get_throws(docstring),
        "todo": parse_docstring_functions.get_todo(docstring),
        "version": parse_docstring_functions.get_version(docstring)
    }
