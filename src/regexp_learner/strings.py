#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of the regexp-learner project
# https://github.com/nokia/regexp-learner

def prefixes(s: str) -> iter:
    """
    Lists all the prefixes of an arbitrary string
    (including the empty word).

    Example:
        >>> from regexp_learner import prefixes
        >>> sorted(prefixes("abcd"))
        ['', 'a', 'ab', 'abc', 'abcd']

    Args:
        s (str): A ``str`` instance.

    Returns:
        The prefixes of ``s``.
    """
    return (s[:i] for i in range(len(s) + 1))

def is_prefix_closed(strings: set) -> bool:
    """
    Tests whether a set of strings is prefix-closed (i.e., all the prefixes
    of all the strings belong to this set).

    Example:
        >>> from regexp_learner import is_prefix_closed
        >>> is_prefix_closed({"", "a", "ab", "abc"})
        True
        >>> is_prefix_closed({"xy", "xyz"})
        False

    Args:
        strings (set): A set of strings.

    Returns:
        ``True`` iff ``strings`` is prefix-closed, ``False`` otherwise.
    """
    return not any(
        prefix not in strings
        for s in strings
        for prefix in prefixes(s)
    )

def suffixes(s: str):
    """
    Lists all the suffixes of an arbitrary string
    (including the empty word).

    Example:
        >>> from regexp_learner import suffixes
        >>> sorted(suffixes("abcd"))
        ['', 'abcd', 'bcd', 'cd', 'd']

    Args:
        s (str): A ``str`` instance.

    Returns:
        The suffixes of ``s``.
    """
    return (s[i:] for i in range(len(s) + 1))

def is_suffix_closed(str_set) -> bool:
    """
    Tests whether a set of strings is suffix-closed (i.e., all the suffixes
    of all the strings belong to this set).

    Example:
        >>> from regexp_learner import is_suffix_closed
        >>> is_suffix_closed({"", "abc", "bc", "c"})
        True
        >>> is_suffix_closed({"xy", "xyz"})
        False

    Args:
        strings (set): A set of strings.

    Returns:
        ``True`` iff ``strings`` is suffix-closed, ``False`` otherwise.
    """

    return not any(
        suffix not in str_set
        for s in str_set
        for suffix in suffixes(s)
    )
