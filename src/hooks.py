import inspect
import typing

class HookException(Exception):
    """ Error to raise in the event a hook issue cannot be adequately resolved."""
    def __init__(self, message):
        super().__init__(message)

class Hooks():
    def __init__(self) -> None:
        self._registered: dict[dict[list[int]]] = {}
        self.doing: dict = {"hook_name": None, "callback": None, "priority": None}
        self.done: list|None = []

    def add(self, hook_name: str, callback: typing.Callable, priority: int = 10) -> True:
        """ Register a new hook.
            @param hook_name The identifying name for the hook
            @param callback A callable function to execute when this hook fires
            @param priority The priority level within this hook name. Hooks will execute in order of priority level
                followed by the order in which they were registered within that priority. This value must be coercible
                to an integer that is greater than or equal 0.
            @throws [HookException] If priority is less than 0 or is not coercible to an integer 
            @returns True if the hook was found and removed            
            @example
            Hooks.add("my_hook_name", my_callback_function, 10) 
            Hooks.add("my_hook_name", my_callback_function, 5) 
            Hooks.add("my_hook_name", my_callback_function) # Implicitly assumes priority 10
            Hooks.add("my_hook_name", my_callback_function, 755) 
        """

        try:
            priority = round(float(priority))
        except:
            try:
                priority = int(priority)
            except:
                raise HookException("Hook priority value must be type integer or float.")

        if int(priority) < 0:
            raise HookException("Hook priority value must be an integer greater than or equal to 0.")

        args = inspect.getfullargspec(callback).args
        if len(args) > 1:
            raise HookException("Hooks may only take a single argument. Use a list/tuple/dict for more args.")

        if hook_name in self._registered:
            if priority in self._registered[hook_name]:
                self._registered[hook_name][priority].append(callback) # Hook and priority already existed
            else:
                self._registered[hook_name][priority] = [callback] # Hook priority did not exist
        else:
            self._registered[hook_name] = {priority: [callback]} # Hook didn't exist

        return True

    def remove(self, hook_name: str, callback: typing.Callable, priority: int = 10) -> bool:
        """ Remove a callback from a hook. The hook to remove must exactly match the name, callable, and priority.

            If a hook matching these conditions is not met, it will do nothing and throw no errors.

            @param hook_name The identifying name for the hook to remove
            @param callback The callable function registered under this hook
            @param priority The priority level for the hook to be removed
            @returns True if the hook was found and removed, False otherwise
            @example
            Hooks.remove("my_hook_name", my_callback_function, 10)
            Hooks.remove("my_hook_name", my_callback_function, 5)
            Hooks.remove("my_hook_name", my_callback_function) # Implicitly assumes priority 10
        """

        try:
            hook_name = str(hook_name)
            priority = int(priority)

            # Try to remove callback
            self._registered[hook_name][priority].remove(callback)

            # Try to remove priority if there are no more under this dict
            if len(self._registered[hook_name][priority]) == 0:
                del self._registered[hook_name][priority]

            # Try to remove hook if there are no more under this dict
            if len(self._registered[hook_name]) == 0:
                del self._registered[hook_name]

            return True
        except:
            return False

    def remove_all(self, hook_name: str, priority: int|None = None) -> bool:
        """ Remove all callbacks from a specified hook and optional priority.

            If no hooks matching these conditions are found, it will do nothing and throw no errors.

            @param hook_name The identifying name for the hook to remove
            @param priority The optional priority level for the hook to be removed. If omitted, this function will
                remove all callbacks in a hook name of all priorities. If included, the function will delete only those
                with that priority level.
            @returns True if the hooks were found and removed, False otherwise
            @example
            Hooks.remove_all("my_hook_name")
            Hooks.remove_all("my_hook_name", 22)
        """

        try:
            hook_name = str(hook_name)
            
            # Try to remove priority if there are no more under this dict, otherwise remove whole dict
            if priority is not None:
                priority = int(priority)
                del self._registered[hook_name][priority]
            else:
                del self._registered[hook_name]

            return True
        except:
            return False
    
    def has(self, hook_name: str, priority: int|None = None, callback: typing.Callable|None = None) -> bool:
        """ Checks if this Hooks class instance has any hook registered meeting these criteria. 

            If no hooks matching these conditions are found, it will do nothing and throw no errors.

            @param hook_name The identifying name for the hook to check for
            @param callback The callback function to check for
            @param priority The priority level for the hook to check for
            @returns True if the hooks were found and removed, False otherwise
            @example
            Hooks.has("my_hook_name")
            Hooks.has("my_hook_name", 719)
            Hooks.has("my_hook_name", 719, my_callback_function)
        """
        try:
            # If not coercible to an integer, abort early
            if priority is not None:
                priority = int(float(priority))
        except:
            return False

        if hook_name in self._registered:
            if priority is None:
                return True
            elif priority in self._registered[hook_name]:
                if callback is None:
                    return True
                else:
                    if callback in self._registered[hook_name][priority]:
                        return True
                    return False
            else:
                return False
        else:
            return False
