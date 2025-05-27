#!/usr/bin/env pytest
# -*- coding: utf-8 -*-
#
# This file is part of the regexp-learner project
# https://github.com/nokia/regexp-learner

from regexp_learner import GoldObservationTable


def test_gold_observation_table1():
    s_plus = s_minus = ["a"]
    sigma = "a"
    try:
        GoldObservationTable(
            s_plus,
            s_minus,
            sigma
        )
        assert False
    except Exception:
        assert True


def test_gold_observation_table2():
    s_plus = ["a"]
    s_minus = []
    sigma = ""
    try:
        GoldObservationTable(
            s_plus,
            s_minus,
            sigma
        )
        assert False
    except Exception:
        assert True


def test_gold_observation_table3():
    s_plus = ["a"]
    s_minus = []
    sigma = ""
    red_states = ["a"]
    try:
        GoldObservationTable(
            s_plus,
            s_minus,
            sigma=sigma,
            red_states=red_states
        )
        assert False
    except Exception:
        assert True


def test_gold_observation_table4():
    s_plus = ["a"]
    s_minus = []
    sigma = "a"
    GoldObservationTable(
        s_plus,
        s_minus,
        sigma=sigma
    )
