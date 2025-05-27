#!/usr/bin/env pytest
# -*- coding: utf-8 -*-
#
# This file is part of the regexp-learner project
# https://github.com/nokia/regexp-learner

from regexp_learner.strings import (
    prefixes,
    suffixes,
    is_prefix_closed,
    is_suffix_closed,
)


def test_prefixes():
    obtained = set(prefixes("abcd"))
    expected = {"abcd", "abc", "ab", "a", ""}
    assert obtained == expected


def test_suffixes():
    obtained = set(suffixes("abcd"))
    expected = {"abcd", "bcd", "cd", "d", ""}
    assert obtained == expected


def test_is_prefix_closed():
    strings = set(prefixes("abcd"))
    assert is_prefix_closed(strings) is True, sorted(strings)

    strings.add("xyz")
    assert is_prefix_closed(strings) is False, sorted(strings)

    strings.remove("xyz")
    strings.remove("abc")
    assert is_prefix_closed(strings) is False, sorted(strings)


def test_is_suffix_closed():
    strings = set(suffixes("abcd"))
    assert is_suffix_closed(strings) is True, sorted(strings)

    strings.add("xyz")
    assert is_suffix_closed(strings) is False, sorted(strings)

    strings.remove("xyz")
    strings.remove("bcd")
    assert is_suffix_closed(strings) is False, sorted(strings)
