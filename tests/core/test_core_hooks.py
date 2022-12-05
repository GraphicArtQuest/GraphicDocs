import unittest

import pprint

from src.core import Core
from src.core import Hooks, HookException

pp = pprint.PrettyPrinter(indent= 4, width=180) # As needed for debugging the test code
        # pp.pprint(hooks._registered)

class TestCoreHooks(unittest.TestCase):

    def callback_action(self):
        print("I am a test action.")

    ###############################################################
    # Base Hook Class - Add
    ###############################################################

    def test_hooks_add_accepts_good_single_hook_priority_omitted(self):
        """Adding good hooks to the list with optional parameter omitted."""
        hooks = Hooks()
        
        expected = {
            "the_test_hook": {
                10: [self.callback_action]
            }
        }
        received = hooks._registered

        self.assertTrue(hooks.add("the_test_hook", self.callback_action))
        self.assertEqual(expected, received)
    
    def test_hooks_add_accepts_good_single_hook_priority_specified(self):
        """Adding good hooks to the list with all values specified."""
        hooks = Hooks()
        
        expected = {
            "the_test_hook": {
                42: [self.callback_action]
            }
        }
        received = hooks._registered

        self.assertTrue(hooks.add("the_test_hook", self.callback_action, 42))
        self.assertEqual(expected, received)

    def test_hooks_add_accepts_good_single_hook_priority_less_than_0_throws_error(self):
        """Adding hooks to the list with negative priority throws an error."""
        hooks = Hooks()

        with self.assertRaises(HookException):
            hooks.add("the_test_hook", self.callback_action, -2)

    def test_hooks_add_accepts_good_single_hook_priority_not_coercible_to_int_throws_error(self):
        """Adding hooks to the list with non-coercible priority throws an error."""
        
        priorities = [
            "Hi there",
            {"a": "Some String"},
            ["A", "B", "C"],
            ["Some String"],
            ("A", "B", "C"),
            None,
            str,    # Class references
            unittest,   # Module references
            Core._process_user_defined_config   # Function references
        ]
        for priority in priorities:
            with self.assertRaises(HookException):
                hooks = Hooks()
                hooks.add("the_test_hook", self.callback_action, priority)

    def test_hooks_with_priorities_that_are_coercible_get_added(self):
        """Adding good hooks to the list."""
        self.maxDiff = None
        hooks = Hooks()
        
        self.assertTrue(hooks.add("the_test_hook", self.callback_action, True))
        self.assertTrue(hooks.add("the_test_hook", self.callback_action, False))
        self.assertTrue(hooks.add("the_test_hook", self.callback_action, 0))
        self.assertTrue(hooks.add("the_test_hook", self.callback_action, "1"))
        self.assertTrue(hooks.add("the_test_hook", self.callback_action, 2))
        
        self.assertTrue(hooks.add("the_test_hook", self.callback_action, 5.9))
        self.assertTrue(hooks.add("the_test_hook", self.callback_action, 6.4))
        self.assertTrue(hooks.add("the_test_hook", self.callback_action))
        self.assertTrue(hooks.add("the_test_hook", self.callback_action))
        self.assertTrue(hooks.add("the_test_hook", self.callback_action))
        self.assertTrue(hooks.add("the_test_hook", self.callback_action, 9.5))

        
        self.assertTrue(hooks.add("the_test_hook", self.callback_action, "500000.9123584"))
        self.assertTrue(hooks.add("the_test_hook", self.callback_action, "500001.49"))

        expected = {
            "the_test_hook": {
                0: [self.callback_action, self.callback_action],
                1: [self.callback_action, self.callback_action],
                2: [self.callback_action],
                6: [self.callback_action, self.callback_action],
                10: [self.callback_action, self.callback_action, self.callback_action, self.callback_action],
                500001: [self.callback_action, self.callback_action],
            }
        }
        received = hooks._registered

        self.assertEqual(expected, received)

    def test_hooks_add_accepts_good_values(self):
        """Adding good hooks to the list."""
        self.maxDiff = None
        hooks = Hooks()
        
        self.assertTrue(hooks.add("the_test_hook", self.callback_action, 5))
        self.assertTrue(hooks.add("the_test_hook", self.callback_action, 5))
        self.assertTrue(hooks.add("the_test_hook", self.callback_action, 10))

        expected = {
            "the_test_hook": {
                5: [self.callback_action, self.callback_action],
                10: [self.callback_action]
            }
        }
        received = hooks._registered

        self.assertEqual(expected, received)


    ###############################################################
    # Base Hook Class - Remove
    ###############################################################

    def test_hooks_remove_works_with_good_input(self):
        """Trying to remove a hook with correct data should succeed."""

        self.maxDiff = None
        hooks = Hooks()
        
        hooks.add("the_test_hook1", self.callback_action, 5)
        hooks.add("the_test_hook2", self.callback_action, 8)
        hooks.add("the_test_hook3", self.callback_action, 10)

        expected = {
            "the_test_hook2": {8: [self.callback_action]},
            "the_test_hook3": {10: [self.callback_action]}
        }
        received = hooks._registered

        self.assertTrue(hooks.remove("the_test_hook1", self.callback_action, 5))
        self.assertEqual(expected, received)
        
        expected = {
            "the_test_hook2": {8: [self.callback_action]}
        }
        self.assertTrue(hooks.remove("the_test_hook3", self.callback_action))   # Default priority assumed
        self.assertEqual(expected, received)
        
        expected = {}
        self.assertTrue(hooks.remove("the_test_hook2", self.callback_action, 8))
        self.assertEqual(expected, received)

    def test_hooks_remove_does_not_work_with_input(self):
        """Trying to remove a hook with incorrect data should not succeed."""

        self.maxDiff = None
        hooks = Hooks()
        
        hooks.add("the_test_hook1", self.callback_action, 5)
        hooks.add("the_test_hook2", self.callback_action, 8)
        hooks.add("the_test_hook3", self.callback_action, 10)

        expected = {
            "the_test_hook1": {5: [self.callback_action]},
            "the_test_hook2": {8: [self.callback_action]},
            "the_test_hook3": {10: [self.callback_action]}
        }
        received = hooks._registered

        self.assertFalse(hooks.remove("the_test_hook1", self.callback_action))  # Priority wrong
        self.assertEqual(expected, received)
        
        self.assertFalse(hooks.remove("the_test_hook2", self.callback_action, 5))   # Name wrong
        self.assertEqual(expected, received)
        
        self.assertFalse(hooks.remove("the_test_hook3", Core.validate_filepath, 10))   # Callback wrong
        self.assertEqual(expected, received)
        
        self.assertFalse(hooks.remove("bad_name", Core.validate_filepath))   # Bad name and Callback wrong
        self.assertEqual(expected, received)

        self.assertFalse(hooks.remove("the_test_hook1", self.callback_action, -135))  # Negative priority
        self.assertEqual(expected, received)

    def test_hooks_remove_some_while_leaving_others_in_same_hook_and_priority(self):
        """Trying to remove a hook with others in the same priority should selectively remove only the chosen one."""

        self.maxDiff = None
        hooks = Hooks()
        
        hooks.add("the_test_hook", self.callback_action, 5.9)
        hooks.add("the_test_hook", self.callback_action, 6.4)
        hooks.add("the_test_hook", self.callback_action)
        hooks.add("the_test_hook", Core.validate_filepath)  # Just using various functions as callbacks for testing
        hooks.add("the_test_hook", unittest.findTestCases)

        expected = {
            "the_test_hook": {
                6: [self.callback_action],
                10: [self.callback_action, Core.validate_filepath, unittest.findTestCases],
            }
        }
        received = hooks._registered

        self.assertTrue(hooks.remove("the_test_hook", self.callback_action, 6)) # Only deleted one of two identical
        self.assertEqual(expected, received)

        
        expected = {
            "the_test_hook": {
                6: [self.callback_action],
                10: [self.callback_action, unittest.findTestCases],
            }
        }
        self.assertTrue(hooks.remove("the_test_hook", Core.validate_filepath, 10)) # Deleted unique one
        self.assertEqual(expected, received)

    def test_hooks_trying_to_include_bad_priority_does_not_work(self):
        """Trying to remove a hook with others in the same priority should selectively remove only the chosen one."""

        self.maxDiff = None
        hooks = Hooks()
        
        hooks.add("the_test_hook", self.callback_action, 5.9)
        hooks.add("the_test_hook", Core.validate_filepath, 6.4)
        hooks.add("the_test_hook", self.callback_action, 10)
        hooks.add("the_test_hook", Core.validate_filepath)  # Just using various functions as callbacks for testing
        hooks.add("the_test_hook", unittest.findTestCases)

        expected = {
            "the_test_hook": {
                6: [self.callback_action, Core.validate_filepath],
                10: [self.callback_action, Core.validate_filepath, unittest.findTestCases],
            }
        }
        received = hooks._registered

        self.assertFalse(hooks.remove("the_test_hook", Core.validate_filepath, "abc")) # Priority not an integer
        self.assertEqual(expected, received)
        
        expected = {
            "the_test_hook": {
                6: [self.callback_action],
                10: [self.callback_action, Core.validate_filepath, unittest.findTestCases],
            }
        }
        self.assertTrue(hooks.remove("the_test_hook", Core.validate_filepath, "6")) # Priority coercible to integer
        self.assertEqual(expected, received)


    ###############################################################
    # Base Hook Class - Remove All
    ###############################################################

    def test_hooks_remove_all_works_with_good_input(self):
        """Trying to remove all callbacks within a hook by name should work"""

        self.maxDiff = None
        hooks = Hooks()
        
        hooks.add("the_test_hook1", self.callback_action, 1)
        hooks.add("the_test_hook1", self.callback_action, 2)
        hooks.add("the_test_hook1", self.callback_action, 2)
        hooks.add("the_test_hook1", self.callback_action, 2)
        hooks.add("the_test_hook1", self.callback_action, 3)

        hooks.add("the_test_hook2", self.callback_action, 11)
        hooks.add("the_test_hook2", self.callback_action, 12)
        hooks.add("the_test_hook2", self.callback_action, 13)

        hooks.add("the_test_hook3", self.callback_action, 45)
        hooks.add("the_test_hook3", self.callback_action, 46)
        hooks.add("the_test_hook3", self.callback_action, 47)

        expected = {
            "the_test_hook1": {
                1: [self.callback_action],
                3: [self.callback_action],
            },
            "the_test_hook2": {
                11: [self.callback_action],
                12: [self.callback_action],
                13: [self.callback_action],
            },
            "the_test_hook3": {
                45: [self.callback_action],
                46: [self.callback_action],
                47: [self.callback_action],
            }
        }
        received = hooks._registered

        self.assertTrue(hooks.remove_all("the_test_hook1", 2))
        self.assertEqual(expected, received)
        
        self.assertFalse(hooks.remove_all("the_test_hook1", 2))  # Nothing should happen because nothing is there
        self.assertFalse(hooks.remove_all("the_test_hook1", 222))  # Nothing should happen because nothing is there
        self.assertEqual(expected, received)
        
        self.assertFalse(hooks.remove_all("the_test_hook1", "2"))   # Bad value for priority, does nothing
        self.assertEqual(expected, received)
        
        
        expected = {
            "the_test_hook1": {
                1: [self.callback_action],
                3: [self.callback_action],
            },
            "the_test_hook3": {
                45: [self.callback_action],
                46: [self.callback_action],
                47: [self.callback_action],
            }
        }
        self.assertTrue(hooks.remove_all("the_test_hook2")) # Omitting priority, should delete all
        self.assertEqual(expected, received)
        
        
    ###############################################################
    # Base Hook Class - Has
    ###############################################################

    def test_hooks_has_finds_correct_values(self):
        """Trying to remove all callbacks within a hook by name should work"""

        self.maxDiff = None
        hooks = Hooks()
        
        hooks.add("the_test_hook1", self.callback_action, 1)
        hooks.add("the_test_hook1", self.callback_action, 2)
        hooks.add("the_test_hook1", self.callback_action, 2)
        hooks.add("the_test_hook1", self.callback_action, 2)
        hooks.add("the_test_hook1", Core.validate_filepath, 3)

        hooks.add("the_test_hook2", self.callback_action, 11)
        hooks.add("the_test_hook2", self.callback_action, 12)
        hooks.add("the_test_hook2", self.callback_action, 13)

        hooks.add("the_test_hook3", self.callback_action, 45)
        hooks.add("the_test_hook3", self.callback_action, 46)
        hooks.add("the_test_hook3", self.callback_action, 47)

        self.assertTrue(hooks.has("the_test_hook1"))
        self.assertTrue(hooks.has("the_test_hook2"))
        self.assertTrue(hooks.has("the_test_hook3"))
        self.assertFalse(hooks.has("the_test_hook4"))

        self.assertTrue(hooks.has("the_test_hook1", 1))
        self.assertTrue(hooks.has("the_test_hook1", 2))
        self.assertTrue(hooks.has("the_test_hook1", 3))
        self.assertFalse(hooks.has("the_test_hook1", 4))
        
        self.assertTrue(hooks.has("the_test_hook1", 1, self.callback_action))
        self.assertTrue(hooks.has("the_test_hook1", 2, self.callback_action))
        self.assertFalse(hooks.has("the_test_hook1", 3, self.callback_action))
        self.assertTrue(hooks.has("the_test_hook1", 3, Core.validate_filepath))

        self.assertFalse(hooks.has("the_test_hook46574", 6543, Core.validate_filepath)) # Multiple not present

        # Try to lookup without priority, Only checks for hook1:
        self.assertTrue(hooks.has(hook_name="the_test_hook1", callback=self.callback_action))
        self.assertTrue(hooks.has(hook_name="the_test_hook1"))
    
    def test_hooks_has_returns_false_with_invalid_inputs(self):
        """Trying to remove all callbacks within a hook by name should work"""

        self.maxDiff = None
        hooks = Hooks()
        
        hooks.add("the_test_hook1", self.callback_action, 2)
        hooks.add("the_test_hook2", self.callback_action, 0)

        self.assertFalse(hooks.has("the_test_hook1", "1"))
        self.assertFalse(hooks.has("the_test_hook1", "1.6", self.callback_action))  # Truncates to 1
        self.assertTrue(hooks.has("the_test_hook1", "2", self.callback_action))
        self.assertTrue(hooks.has("the_test_hook1", "2.9", self.callback_action))   # Truncates to 2
        self.assertFalse(hooks.has("the_test_hook1", "5.5"))
        
        self.assertFalse(hooks.has("the_test_hook1", "abc"))
        self.assertFalse(hooks.has("the_test_hook1", self.callback_action)) # Priority can't be callback function
        self.assertTrue(hooks.has("the_test_hook2", False)) # False coerces to priority of 0
        self.assertFalse(hooks.has("the_test_hook2", True)) # True coerces to priority of 1, which is not in the hook
