#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Maxime Raynal"
__maintainer__ = "Maxime Raynal"
__email__ = "maxime.raynal@nokia.com"
__copyright__ = "Copyright (C) 2020, Nokia"
__license__ = "BSD-3"


from collections import defaultdict
from pybgl.property_map import make_assoc_property_map
from pybgl.automaton import make_automaton
from veggie.incidence_node_automaton import IncidenceNodeAutomaton, \
    num_vertices, set_final
from newdle.nlp.trie import delta_best_effort


class GoldObservationTable:
    ZERO = 0
    ONE = 1
    STAR = '*'

    def __init__(
            self,
            s_plus,   # Iterable[str]
            s_minus,  # Iterable[str]
            sigma='abcdefghijklmnopqrstuvwxyz0123456789 ',
            red_states={''},
            fill_holes=False,
            blue_state_choice_func=lambda s: min(s),
            red_state_choice_func=lambda s: min(s),
    ):
        """Initialises the observation table for gold's algorithm
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
        """
        self.check_input_consistency(s_plus, s_minus, sigma, red_states)

        self.blue_state_choice_func = blue_state_choice_func
        self.red_state_choice_func = red_state_choice_func
        self.fill_holes = fill_holes
        self.s_plus = set(s_plus)
        self.s_minus = set(s_minus)
        self.sigma = sigma
        self.exp = sorted(list(  # build suffix closed set EXP
            set(suffix for string in s_plus
                for suffix in suffixes(string)) |
            set(suffix for string in s_minus
                for suffix in suffixes(string))
        ), key=lambda a: (len(a), a))
        self.row_length = len(self.exp)
        self.red_states = {
            prefix: [
                self.get_value_from_sample(prefix + suffix)
                for suffix in self.exp
            ] for prefix in red_states
        }
        self.blue_states = {
            prefix + a: [
                self.get_value_from_sample(prefix + a + suffix)
                for suffix in self.exp
            ] for prefix in red_states
            for a in sigma
            if prefix + a not in red_states
        }

    def check_input_consistency(self, s_plus, s_minus, sigma, red_states):
        # check that all strings have their letters in sigma
        for str_set in [s_plus, s_minus, red_states]:
            for string in str_set:
                if any(char not in sigma for char in string):
                    raise Exception("GoldObservationTable: Error! Some chars "
                                    "are present in samples, "
                                    "but not in the alphabet")
        # check that the red states are prefix closed
        if not is_prefix_closed(red_states):
            raise Exception("GoldObservationTable: Error! the set of red"
                            " states must be prefix-closed.")
        # check that s_plus and s_minus are disjoint
        if any(string in s_plus for string in s_minus) \
           or any(string in s_minus for string in s_plus):
            raise Exception("GoldObservationTable: Error! S+ and S- must"
                            " be disjoint")

    def get_value_from_sample(self, string):
        if string in self.s_plus:
            return self.ONE
        elif string in self.s_minus:
            return self.ZERO
        else:
            return self.STAR

    def is_obviously_different(self, row_1: list, row_2: list):
        return any(
            (row_1[i] == 1 and row_2[i] == 0) or
            (row_1[i] == 1 and row_2[i] == 0)
            for i in range(self.row_length)
        )

    def choose_obviously_different_blue_state(self):
        blue_candidates = [
            blue_state
            for blue_state, blue_state_val in self.blue_states.items()
            if all(self.is_obviously_different(blue_state_val, red_state_val)
                   for red_state_val in self.red_states.values())
        ]
        if len(blue_candidates) == 0:
            return None
        else:
            return self.blue_state_choice_func(blue_candidates)

    def try_and_promote_blue(self):
        blue_to_promote = self.choose_obviously_different_blue_state()
        if blue_to_promote is None:
            return False
        self.red_states[blue_to_promote] = self.blue_states.pop(blue_to_promote)
        for a in self.sigma:
            if blue_to_promote + a not in self.red_states:
                self.blue_states[blue_to_promote + a] = [
                    self.get_value_from_sample(blue_to_promote + a + suffix)
                    for suffix in self.exp
                ]
        return True

    def choose_compatible_red_state(self, row):
        candidates = [
            red_state
            for red_state, red_state_val in self.red_states.items()
            if not self.is_obviously_different(row, red_state_val)
        ]
        if len(candidates) == 0:
            return None
        return self.red_state_choice_func(candidates)

    def try_and_fill_holes(self):
        if not self.fill_holes:
            return True
        for blue_state, blue_state_val in self.blue_states.items():
            red_state = self.choose_compatible_red_state(blue_state_val)
            if red_state is None:  # this should never happen
                return False
            red_state_val = self.red_states[red_state]
            self.red_states[red_state] = [
                red_state_val[i] if red_state_val[i] != self.STAR
                else blue_state_val[i]
                for i in range(self.row_length)
            ]
        self.red_states = {
            red_state: [
                1 if red_state_val[i] != 0 else 0
                for i in range(self.row_length)
            ] for red_state, red_state_val in self.red_states.items()
        }
        for blue_state, blue_state_val in self.blue_states.items():
            red_state = self.choose_compatible_red_state(blue_state_val)
            if red_state is None:
                return False
            self.blue_states[blue_state] = [
                blue_state_val[i] if blue_state_val[i] != self.STAR
                else self.red_states[red_state][i]
                for i in range(self.row_length)
            ]
        return True

    def gold_make_automaton(self):
        """

        """
        if self.fill_holes:
            if not self.try_and_fill_holes():
                return False, self.gold_make_pta()
        epsilon_idx = self.exp.index('')
        states = sorted(list(self.red_states.keys()), key=lambda s: (len(s), s))

        transitions = []
        if self.fill_holes:
            for q in states:
                for a in self.sigma:
                    qa_val = self.red_states.get(
                        q + a,
                        self.blue_states.get(q + a, None)
                    )
                    for r, r_val in self.red_states.items():
                        if qa_val == r_val:
                            transitions += [(q, r, a)]
                            break
        else:
            for q in states:
                for a in self.sigma:
                    if q + a in states:
                        transitions += [(q, q + a, a)]
                    else:
                        qa_val = self.blue_states.get(q + a, None)
                        r = self.choose_compatible_red_state(qa_val)
                        transitions += [(q, r, a)]
        transitions = [
            (states.index(q), states.index(r), a)
            for (q, r, a) in transitions
        ]
        final_states = defaultdict(bool, {
            states.index(state): True
            if self.red_states[state][epsilon_idx] == self.ONE
            else False
            for state in states
        })
        print(final_states)
        print(transitions)
        g = make_automaton(
            transitions,
            states.index(''),
            make_assoc_property_map(final_states)
        )
        if not self.fill_holes:
            if not self.is_consistent_with_samples(g):
                return False, self.gold_make_pta()
        return True, g

    def gold_make_pta(self):
        # TODO move incidence_node_automaton_insert_string into veggie or pybgl
        # and use a method or function from the package rather than from here
        g = IncidenceNodeAutomaton()
        for string in self.s_plus:
            incidence_node_automaton_insert_string(g, string)
        return g

    def is_consistent_with_samples(self, g):
        return True

    def to_html(self):
        def str_to_html(s):
            return repr(s) if s else "&#x3b5;"

        def str_to_red_html(s):
            return "<font color='red'>%s</font>" % str_to_html(s)

        def str_to_blue_html(s):
            return "<font color='blue'>%s</font>" % str_to_html(s)

        return "<table> {header} {rows} </table>".format(
            header="<tr><th></th>%s</tr>" % (
                ''.join(
                    "<td>%s</td>" % str_to_html(suffix)
                    for suffix in self.exp
                )
            ),
            rows=''.join(
                "<tr><th>{prefix}</th>{values}</tr>".format(
                    prefix=str_to_red_html(red_state),
                    values=''.join(
                        "<td>%s</td>" % self.red_states[red_state][i]
                        for i in range(self.row_length)
                    )
                ) for red_state in self.red_states
            ) + ''.join(
                "<tr><th>{prefix}</th>{values}</tr>".format(
                    prefix=str_to_blue_html(blue_state),
                    values=''.join(
                        "<td>%s</td>" % self.blue_states[blue_state][i]
                        for i in range(self.row_length)
                    )
                ) for blue_state in self.blue_states
            )
        )


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
                       if b is False, then the PTA corresponding
                       to s_plus is returned
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
        pass
    return obs_table.gold_make_automaton()


def prefixes(s: str):
    return (s[:i] for i in range(len(s) + 1))


def is_prefix_closed(str_set) -> bool:
    return not any(
        prefix not in str_set
        for s in str_set
        for prefix in prefixes(s)
    )


def suffixes(s: str):
    return (s[i:] for i in range(len(s) + 1))


def is_suffix_closed(str_set) -> bool:
    return not any(
        suffix not in str_set
        for s in str_set
        for suffix in suffixes(s)
    )


def incidence_node_automaton_insert_string(
        g: IncidenceNodeAutomaton, w: str
) -> int:
    if num_vertices(g) == 0:
        g.add_vertex(None)
    (q, i) = delta_best_effort(g, w)
    for a in w[i:]:
        r = g.add_vertex(a)
        g.add_edge(q, r)
        q = r
    set_final(q, g)
    return q
