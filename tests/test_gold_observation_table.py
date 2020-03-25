#!/usr/bin/env pytest
# -*- coding: utf-8 -*-

__author__ = "Maxime Raynal"
__maintainer__ = "Maxime Raynal"
__email__ = "maxime.raynal@nokia.com"
__copyright__ = "Copyright (C) 2020, Nokia"
__license__ = "BSD-3"

from gold_inference.gold_observation_table import GoldObservationTable


def test_gold_observation_table_check_input_consistency():
    s_plus = s_minus = ['a']
    sigma = 'a'
    try:
        obs_table = GoldObservationTable(
            s_plus,
            s_minus,
            sigma
        )
        assert False
    except Exception:
        assert True

    s_minus = []
    sigma = ''
    try:
        obs_table = GoldObservationTable(
            s_plus,
            s_minus,
            sigma
        )
        assert False
    except Exception:
        assert True

    red_states = ['a']
    try:
        obs_table = GoldObservationTable(
            s_plus,
            s_minus,
            sigma=sigma,
            red_states=red_states
        )
        assert False
    except Exception:
        assert True

    s_plus = ['a']
    s_minus = []
    sigma = 'a'
    try:
        obs_table = GoldObservationTable(
            s_plus,
            s_minus,
            sigma=sigma
        )
    except Exception:
        assert False
