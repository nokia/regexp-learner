#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of the regexp-learner project
# https://github.com/nokia/regexp-learner

from pybgl.automaton import Automaton
from pybgl.html import html
from .observation_table import GoldObservationTable

def gold(
    s_plus: iter,
    s_minus: iter,
    sigma: str ="abcdefghijklmnopqrstuvwxyz0123456789 ",
    red_states: set = {""},
    fill_holes: bool = False,
    blue_state_choice_func: callable = min,
    red_state_choice_func: callable = min,
    verbose: bool = False,
) -> tuple:
    """
    Runs the GOLD algorithm.

    Args:
        s_plus (iter): An iterable of strings that are
                present in the language to infer.

        s_minus (iter): An iterable of strings that are
             not present in the language to infer.

        sigma (str): An iterable of chars, represents the alphabet.

        red_states (set): An iterable of strings, should remain default
            to run Gold algorithm.

        fill_holes (bool):
            If ``True``, the function uses the filling holes method.
            If ``False``, the function won't fill holes in the table,
            but search for compatible successors when building
            the automaton.

        blue_state_choice_func (callable): A ``Iterable[str] -> str``
            function, used to choose which blue state to promote
            among the candidates.

        red_state_choice_func (callable): A ``Iterable[str] -> str``
            function, used to choose which red state to choose
            among the red_states which are compatible with a blue one.

        verbose (bool): Pass ``True`` to output in HTML
            the important steps of the algorithm.

    Returns:
        A tuple ``(g, success)`` where:
        ``g`` is the inferred  :py:class:`Automaton`;
        ``success`` equals ``True`` iff the algorithm succeeded
        If ``success`` equals ``False``, then ``g`` is the Prefix Tree
        Acceptor (PTA) accepting ``s_plus``.
    """
    obs_table = GoldObservationTable(
        s_plus,
        s_minus,
        sigma,
        red_states=red_states,
        fill_holes=fill_holes,
        blue_state_choice_func=blue_state_choice_func,
        red_state_choice_func=red_state_choice_func,
    )
    if verbose:
        html(obs_table.to_html())
    while obs_table.try_and_promote_blue():
        if verbose:
            html(obs_table.to_html())
    return obs_table.to_automaton()
