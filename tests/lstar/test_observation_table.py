#!/usr/bin/env pytest-3
# -*- coding: utf-8 -*-
#
# This file is part of the regexp-learner project
# https://github.com/nokia/regexp-learner

from pybgl.html import html
from regexp_learner.lstar.observation_table import LstarObservationTable

def test_observation_table_get_set():
    o = LstarObservationTable("ab")
    o.s = {"", "a"}
    o.set("", "", True)
    o.set("a", "", False)
    o.set("b", "", True)
    o.set("aa", "", True)
    o.set("ab", "", False)
    o.set("a", "a", True)
    html(o.to_html())

    assert o.get("a", "")  == False
    assert o.get("b", "")  == True
    assert o.get("aa", "") == True
    assert o.get("ab", "") == False
    assert o.get("a", "a") == True
    assert o.get("", "a")  == None

def test_observation_table_is_closed():
    def check(o, expected):
        is_closed = o.is_closed()
        html(o.to_html())
        html("This observation table is %scomplete" % ("" if is_closed else "<b>not</b> "))
        assert is_closed == expected

    alphabet = "ab"
    o = LstarObservationTable("ab")

    # S = {epsilon}
    o.s.add("")
    o.set("", "", True)
    check(o, False)

    # Probing SA.
    for a in alphabet: o.set(a, "", True)
    check(o, True)

    # Missing rows
    o.set("a", "", False)
    check(o, False)

    # Fixing rows
    o.set("a", "", True)
    check(o, True)

    # Incomplete probing
    o.s.add("a")
    o.set("a", "", True)
    check(o, False)

def test_observation_table_is_consistent():
    def check(o, expected):
        is_consistent = o.is_consistent()
        html(o.to_html())
        html("This observation table is %sconsistent" % ("" if is_consistent else "<b>not</b> "))
        assert is_consistent == expected

    o = LstarObservationTable("ab")
    o.s = {"", "a"}
    o.set("", "", True)
    o.set("a", "", False)
    o.set("b", "", True)
    o.set("aa", "", True)
    o.set("ab", "", False)
    check(o, True)

    o = LstarObservationTable("ab")
    o.s = {"", "a"}
    o.set("", "", True)
    o.set("a", "", True)
    o.set("b", "", True)
    o.set("aa", "", True)
    o.set("ab", "", False)
    check(o, False)

