# Module: _`hooks`_

_Source: [hooks.py](../../src/hooks.py)_


Table of Contents

- [Imports](#imports)
- [Classes](#classes)
    - [HookException](#class-hookexception)
    - [Hooks](#class-hooks)
        - [add](#class-hooksadd)
        - [remove](#class-hooksremove)
        - [remove_all](#class-hooksremove_all)
        - [has](#class-hookshas)

## Imports

*Modules*
- inspect
- typing

----

# Classes

## `HookException`( **`message`** )<a id='class-hookexception'></a>



|Argument |Type |Default | Description
|:---|:---:|:---|:---|
|`message` |`any` | | |



Extends: `Exception`

> Error to raise in the event a hook issue cannot be adequately resolved.


----

## `Hooks`()<a id='class-hooks'></a>



**Class Methods:**

- `add`( **`hook_name`**,  **`callback`**,  _`priority`_ )<a id='class-hooksadd'></a>
    
    
    
    |Argument |Type |Default | Description
    |:---|:---:|:---|:---|
    |`hook_name` |`str` | | The identifying name for the hook|
    |`callback` |`Callable` | | A callable function to execute when this hook fires|
    |`priority` _(Optional)_ |`int` |`10` | The priority level within this hook name. Hooks will execute in order of priority level followed by the order in which they were registered within that priority. This value must be coercible to an integer that is greater than or equal 0.|
    
    
    
    > Register a new hook.
    
    _Source: [hooks.py, lines 15 thru 54](../../src/hooks.py#L15-L54)_
    
    **Returns** -> `True`: True if the hook was found and removed
    
    Examples:
    
    ```python
    Hooks.add("my_hook_name", my_callback_function, 10) 
    Hooks.add("my_hook_name", my_callback_function, 5) 
    Hooks.add("my_hook_name", my_callback_function) # Implicitly assumes priority 10
    Hooks.add("my_hook_name", my_callback_function, 755) 
    ```
    
    
- `remove`( **`hook_name`**,  **`callback`**,  _`priority`_ )<a id='class-hooksremove'></a>
    
    
    
    |Argument |Type |Default | Description
    |:---|:---:|:---|:---|
    |`hook_name` |`str` | | The identifying name for the hook to remove|
    |`callback` |`Callable` | | The callable function registered under this hook|
    |`priority` _(Optional)_ |`int` |`10` | The priority level for the hook to be removed|
    
    
    
    > Remove a callback from a hook. The hook to remove must exactly match the name, callable, and priority.
    >
    > If a hook matching these conditions is not met, it will do nothing and throw no errors.
    
    _Source: [hooks.py, lines 56 thru 88](../../src/hooks.py#L56-L88)_
    
    **Returns** -> `bool`: True if the hook was found and removed, False otherwise
    
    Examples:
    
    ```python
    Hooks.remove("my_hook_name", my_callback_function, 10)
    Hooks.remove("my_hook_name", my_callback_function, 5)
    Hooks.remove("my_hook_name", my_callback_function) # Implicitly assumes priority 10
    ```
    
    
- `remove_all`( **`hook_name`**,  _`priority`_ )<a id='class-hooksremove_all'></a>
    
    
    
    |Argument |Type |Default | Description
    |:---|:---:|:---|:---|
    |`hook_name` |`str` | | The identifying name for the hook to remove|
    |`priority` _(Optional)_ |`int \| None` |`None` | The optional priority level for the hook to be removed. If omitted, this function will remove all callbacks in a hook name of all priorities. If included, the function will delete only those with that priority level.|
    
    
    
    > Remove all callbacks from a specified hook and optional priority.
    >
    > If no hooks matching these conditions are found, it will do nothing and throw no errors.
    
    _Source: [hooks.py, lines 90 thru 117](../../src/hooks.py#L90-L117)_
    
    **Returns** -> `bool`: True if the hooks were found and removed, False otherwise
    
    Examples:
    
    ```python
    Hooks.remove_all("my_hook_name")
    Hooks.remove_all("my_hook_name", 22)
    ```
    
    
- `has`( **`hook_name`**,  _`priority`_,  _`callback`_ )<a id='class-hookshas'></a>
    
    
    
    |Argument |Type |Default | Description
    |:---|:---:|:---|:---|
    |`hook_name` |`str` | | The identifying name for the hook to check for|
    |`priority` _(Optional)_ |`int \| None` |`None` | The priority level for the hook to check for|
    |`callback` _(Optional)_ |`Optional` |`None` | The callback function to check for|
    
    
    
    > Checks if this Hooks class instance has any hook registered meeting these criteria.
    >
    > If no hooks matching these conditions are found, it will do nothing and throw no errors.
    
    _Source: [hooks.py, lines 119 thru 153](../../src/hooks.py#L119-L153)_
    
    **Returns** -> `bool`: True if the hooks were found and removed, False otherwise
    
    Examples:
    
    ```python
    Hooks.has("my_hook_name")
    Hooks.has("my_hook_name", 719)
    Hooks.has("my_hook_name", 719, my_callback_function)
    ```
    
    

----

Visit [Graphic Art Quest](https://www.GraphicArtQuest.com) for more!