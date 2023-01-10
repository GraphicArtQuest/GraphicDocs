# Module: _`core`_

_Source: [core.py](src\core.py)_


Table of Contents

- [Imports](#imports)
- [Classes](#classes)
    - [Core](#class-core)
        - [validate_filepath](#class-corevalidate_filepath)
        - [console](#class-coreconsole)
        - [load_python_module](#class-coreload_python_module)
        - [parse_source_targets](#class-coreparse_source_targets)
        - [build](#class-corebuild)
        - [do_action](#class-coredo_action)
        - [apply_filter](#class-coreapply_filter)
- [Functions](#functions)
    - [FormatForConsole](#formatforconsole)

## Imports

*Modules*
- importlib
- inspect
- json
- os
- plugins
- re
- templates

*Classes*
- Enum (from `enum`)
- Hooks (from `src.hooks`)

*Functions*
- deepcopy (from `copy`)
- parse_module (from `src.parser`)

----

# Classes

## `Core`( _`user_defined_config`_ )<a id='class-core'></a>



|Argument |Type |Default | Description
|:---|:---:|:---|:---|
|`user_defined_config` _(Optional)_ |`str` |`''` | |

**Class Methods:**

- `validate_filepath`()<a id='class-corevalidate_filepath'></a>
    
    
    
    
    
    > Validate a file path by returning a valid absolute file path under any circumstance.
    >
    > For settings that involve file paths, either absolute or relative relative paths are allowed. Use a single dot '.' for the current directory, and a double dot '..' to go up a directory. Absolute paths resolve as themselves.
    
    _Source: [core.py, lines 84 thru 116](src\core.py)_
    
    **Returns** -> `str`: Valid absolute path for generated files.
    
    Examples:
    
    Path Resolution (Working directory is in 'C:\users\GAQ\Working')
    
    ```python
    self.validate_filepath("output")                                    # C:\users\GAQ\Working\output
    self.validate_filepath("C:\users\GAQ\Working\output")           # C:\users\GAQ\Working\output
    self.validate_filepath(".\output")                                 # C:\users\GAQ\Working\output
    self.validate_filepath("..\output")                                # C:\users\GAQ\output
    self.validate_filepath("..\..\output")                            # C:\users\output
    self.validate_filepath(["Bad Path In List Goes To Working Dir"])    # C:\users\GAQ\Working\output
    ```
    
    
- `console`( **`message`**,  _`output_to_console`_ )<a id='class-coreconsole'></a>
    
    
    
    |Argument |Type |Default | Description
    |:---|:---:|:---|:---|
    |`message` |`str` | | The message to log to the console|
    |`output_to_console` _(Optional)_ |`bool` |`True` | If True, this message will log to the console. Otherwise, it won't. It can be useful to set this to false to obtain the pretty formatted error message for use elsewhere. This allows 'verbose' to be on while not outputting this particular text to the console.|
    
    
    
    > Creates pretty formatted text and logs it to the console.
    
    _Source: [core.py, lines 118 thru 142](src\core.py)_
    
    **Returns** -> `str`: A string representation of message
    
    Examples:
    
    ```python
    console("I am a console message.")
    console("I am a 'console' message.")    # Will automatically wrap the quoted text in a green color.
    ```
    
    
- `load_python_module`( **`path_to_module`** )<a id='class-coreload_python_module'></a>
    
    
    
    |Argument |Type |Default | Description
    |:---|:---:|:---|:---|
    |`path_to_module` |`str` | | An absolute or relative path to the module|
    
    
    
    > Loads a python module into memory. If not provided an absolute file path, it will traverse through a series of possible directories to try to resolve it using the following priorities:
    >
    > 1. In or relative to the working directory where the main script was run from 2. The config file directory 3. The system path (e.g. you build and install callable modules as packages using PIP)
    
    _Source: [core.py, lines 300 thru 356](src\core.py)_
    
    **Returns** -> `<built-in function callable>`: A loaded reference to the module
    
    
- `parse_source_targets`( **`target_path`** )<a id='class-coreparse_source_targets'></a>
    
    
    
    |Argument |Type |Default | Description
    |:---|:---:|:---|:---|
    |`target_path` |`str` | | A filesystem path to search and parse. Can be a file or folder.|
    
    
    
    > Parses source files into a list target path. It will search using the exclusion patterns and source folder depth limit.
    >
    > This method runs during initialization, but is designed so that it can be used again later for other purposes. It does not update any core instance settings directly.
    
    _Source: [core.py, lines 464 thru 555](src\core.py)_
    
    **Returns** -> `list`: A list of parsed dictionaries for each file in the source list.
    
    
- `build`()<a id='class-corebuild'></a>
    
    
    
    
    
    > Runs the template's build function while passing the core object to it.
    
    _Source: [core.py, lines 557 thru 574](src\core.py)_
    
    
- `do_action`( **`action_name`**,  _`args`_ )<a id='class-coredo_action'></a>
    
    
    
    |Argument |Type |Default | Description
    |:---|:---:|:---|:---|
    |`action_name` |`str` | | The case sensitive name of the action hook to run|
    |`args` _(Optional)_ |`dict` |`{}` | An optional dictionary of arguments to pass to the callback functions|
    
    
    
    > Executes all actions with the provided name in order of priority.
    
    _Source: [core.py, lines 576 thru 619](src\core.py)_
    
    Examples:
    
    ```python
    testval = 2
    def test_func(input: int)
        nonlocal testval
        testval *= 2
    
    core = Core()
    core.filters.add("test_actions", test_func, 5)
    core.filters.add("test_actions", test_func)
    core.filters.add("test_actions", test_func, 15)
    
    core.apply_filter("test_actions", 2) # testval = 16
    ```
    
    
- `apply_filter`( **`filter_name`**,  **`filter_input`** )<a id='class-coreapply_filter'></a>
    
    
    
    |Argument |Type |Default | Description
    |:---|:---:|:---|:---|
    |`filter_name` |`str` | | The case sensitive name of the filter to apply|
    |`filter_input` |`any` | | An input argument to modify|
    
    
    
    > Applies all filters with the provided name to the provided input sequentially and in order of priority. In most cases, the filtered response should match input format, but this is not strictly necessary.
    
    _Source: [core.py, lines 621 thru 672](src\core.py)_
    
    Examples:
    
    ```python
    def test_func(input: int)
        return input * 2
    
    core = Core()
    core.filters.add("test_filters", test_func, 5)
    core.filters.add("test_filters", test_func)
    core.filters.add("test_filters", test_func, 15)
    
    final_val = core.apply_filter("test_filters", 2) # Returns 16
    ```
    
    

----

# Functions

## `FormatForConsole`( **`message`**,  _`type`_ )<a id='formatforconsole'></a>



|Argument |Type |Default | Description
|:---|:---:|:---|:---|
|`message` |`str` | | The message to apply colored escape codes to|
|`type` _(Optional)_ |`ConsoleColorCodes` |`ConsoleColorCodes.ENDC` | |



> Applies color to a message that will output in the console.

_Source: [core.py, lines 43 thru 50](src\core.py)_

**Returns** -> `str`: The same message wrapped in the appropriate formatting code

----

Visit [Graphic Art Quest](https://www.GraphicArtQuest.com) for more!