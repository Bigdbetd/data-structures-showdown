# Selected question from timed_challenge.txt:
# 13. Balanced Symbols
# Check if the brackets in a string are balanced.
# Input: "{[()]}"
# Output: True
# Input: "{[(])}"
# Output: False

"""Balanced bracket checker using a list as a stack."""

import unittest


def balanced_symbols(text):
    """Check (), [], and {}; ignore other characters; require a string.

    Expected runtime is O(n), with O(n) worst-case auxiliary space.
    This checks bracket nesting, not programming-language string/comment syntax.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    closing_to_opening = {')': '(', ']': '[', '}': '{'}
    opening = set(closing_to_opening.values())
    stack = []

    for character in text:
        if character in opening:
            stack.append(character)
        elif character in closing_to_opening:
            if not stack or stack.pop() != closing_to_opening[character]:
                return False

    return not stack


class BalancedSymbolsTests(unittest.TestCase):
    def test_prompt_examples(self):
        self.assertTrue(balanced_symbols("{[()]}"))
        self.assertFalse(balanced_symbols("{[(])}"))

    def test_empty_and_non_bracket_text(self):
        for text in ["", "hello", " \n\t", "abc123"]:
            with self.subTest(text=text):
                self.assertTrue(balanced_symbols(text))

    def test_nested_adjacent_and_embedded_brackets(self):
        for text in ["()[]{}", "((()))", "[{()}]", "a + (b * [c - {d}])"]:
            with self.subTest(text=text):
                self.assertTrue(balanced_symbols(text))

    def test_unmatched_opening_and_closing(self):
        for text in ["(", "[", "{", ")", "]", "}", "(()", "())", ")("]:
            with self.subTest(text=text):
                self.assertFalse(balanced_symbols(text))

    def test_crossed_and_wrong_bracket_types(self):
        for text in ["(]", "[)", "{]", "([)]", "{[(])}"]:
            with self.subTest(text=text):
                self.assertFalse(balanced_symbols(text))

    def test_wrong_data_types(self):
        for value in [None, 123, 1.5, True, [], ["("], {}, b"()"]:
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    balanced_symbols(value)

    def test_large_input_without_recursion(self):
        self.assertTrue(balanced_symbols("(" * 10000 + ")" * 10000))
        self.assertFalse(balanced_symbols("(" * 10000 + ")" * 9999))

    def test_calls_do_not_share_stack_state(self):
        self.assertFalse(balanced_symbols("("))
        self.assertTrue(balanced_symbols("[]"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
