# @example

## Table of Contents

- [Overview](#overview)
- [Examples](#examples)

## Overview

The `@example` tag provides a way to show an in code example of how to use the function or class.

The tag assumes that everything within it will be code. Therefore, there is no need to use other markdown delimiters such as backticks.

Any text after the `@example` tag will get treated as a caption for the example. Captioned text does NOT roll over to subsequent lines.

## Examples

All lines after the `@example` tag will get treated as a Python code block.

```python
def print_input(my_input) -> None:
    """
        Prints an input to the console.

        @param input Can be any data type
        @example
        # This is a comment within the example
        print_input(2)
        # '2' is printed to the console
    """
    print(my_input)
```

Add captions to the example on the same line as the `@example` tag.

```python
def print_input(my_input) -> None:
    """
        Prints an input to the console.

        @param input Can be any data type
        @example This example has a caption now
        # This is a comment within the example
        print_input(2)
        # '2' is printed to the console
    """
    print(my_input)
```

Add as many `@example` tags as you need.

```python
def print_input(my_input) -> None:
    """
        Prints an input to the console.

        @param input Can be any data type
        @example Integer input
        print_input(2)
        # '2' is printed to the console

        @example Boolean input also works
        print_input(False)
        # 'False' is printed to the console
        
        @example String input works as well
        print_input("Hello World!")
        # 'Hello World!' is printed to the console
    """
    print(my_input)
```

Code indentation is based on the indentation of the `@example` tag in the docstring. It assumes characters beginning at the same position as the `@` character are at code position zero. This allows you to maintain your desired formatting while creating the example.

```python
def print_input(my_input) -> None:
    """
        Prints an input to the console, but only if equal to 2.

        @param input Can be any data type
        
        @example Only print if integer is equal to 2.
        my_var = 1
        print(my_var)
            # Nothing happens
        my_var += 1
        if my_var == 2:
            my_var += 2
            print(my_var)
                # Prints to the console
        
        @returns Just console output
    """
    print(my_input)
```
