#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Maxime Raynal"
__maintainer__ = "Maxime Raynal"
__email__ = "maxime.raynal@nokia.com"
__copyright__ = "Copyright (C) 2020, Nokia"
__license__ = "BSD-3"


from gold_inference.gold_observation_table import GoldObservationTable


def gold_infer_automaton(
        s_plus,   # Iterable[str]
        s_minus,  # Iterable[str]
        sigma='abcdefghijklmnopqrstuvwxyz0123456789 ',
        red_states={''},
        fill_holes=False,
        blue_state_choice_func=lambda s: min(s),
        red_state_choice_func=lambda s: min(s),
) -> tuple:  # (bool, Automaton)
    """
    Runs golds automaton on the given input
        Args:
            s_plus: iterable of strings that are
                    present in the language to infer
            s_minus: iterable of strings that are
                     not present in the language to infer
            sigma: iterable of chars, represents the alphabet
            red_states: iterable of strings, should remain default
                        to run gold's algorithm
            fill_holes: bool.
                     if True, will use the filling holes method
                        if False, will not fill holes in the table
                           but rather search for compatible successors
                           when building the automaton
            blue_state_choice_func: function: Iterable[str] -> str
                       the function used to choose which blue state to promote
                       among the candidates
            red_state_choice_func: function: Iterable[str] -> str
                       the function used to choose which red state to choose
                       among the red_states which are compatible with a blue one
        Returns:
            a tuple (b, g) where
                    b: bool is True if the algorithm succeeded in building
                       an automaton
                       if b is False, then the PTA accepting s_plus is returned
                    g: Automaton if b is True, else NodeAutomaton

    """
    obs_table = GoldObservationTable(
        s_plus,
        s_minus,
        sigma,
        red_states=red_states,
        fill_holes=fill_holes,
        blue_state_choice_func=blue_state_choice_func,
        red_state_choice_func=red_state_choice_func
    )
    while obs_table.try_and_promote_blue():
        print(obs_table.to_html())
    return obs_table.gold_make_automaton()
