#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of the regexp-learner project
# https://github.com/nokia/regexp-learner

from collections import defaultdict
from pybgl.property_map import make_assoc_property_map
from pybgl.automaton import Automaton, make_automaton
from pybgl.trie import Trie
from ..strings import is_prefix_closed, suffixes

class GoldObservationTable:
    """
    The :py:class:`GoldObservationTable` class implements the observation
    table used in the Gold algorithm.
    """
    ZERO = 0
    ONE = 1
    STAR = '*'

    def __init__(
        self,
        s_plus: set,
        s_minus: set,
        sigma :str = 'abcdefghijklmnopqrstuvwxyz0123456789 ',
        red_states: set = {''},
        fill_holes: bool = False,
        blue_state_choice_func: callable = min,
        red_state_choice_func: callable = min,
    ):
        """
        Constructor.

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

            show_tables_as_html (bool): Pass ``True`` to output in HTML
                the important steps of the algorithm.
        """
        GoldObservationTable.check_input_consistency(s_plus, s_minus, sigma, red_states)
        self.blue_state_choice_func = blue_state_choice_func
        self.red_state_choice_func = red_state_choice_func
        self.fill_holes = fill_holes
        self.s_plus = set(s_plus)
        self.s_minus = set(s_minus)
        self.sigma = sigma
        self.exp = sorted(
            list( # Build suffix closed set EXP
                set(
                    suffix
                    for string in s_plus
                    for suffix in suffixes(string)
                ) | set(
                    suffix
                    for string in s_minus
                    for suffix in suffixes(string)
                )
            ),
            key=lambda a: (len(a), a)
        )
        self.row_length = len(self.exp)
        self.red_states = {
            prefix: [
                self.get_value_from_sample(prefix + suffix)
                for suffix in self.exp
            ]
            for prefix in red_states
        }
        self.blue_states = {
            prefix + a: [
                self.get_value_from_sample(prefix + a + suffix)
                for suffix in self.exp
            ]
            for prefix in red_states
            for a in sigma
            if prefix + a not in red_states
        }

    @staticmethod
    def check_input_consistency(s_plus, s_minus, sigma, red_states):
        """
        Checks that the input given to build an observation table is consistent.

        Args:
            s_plus (iter): An iterable of strings that are
                    present in the language to infer.

            s_minus (iter): An iterable of strings that are
                 not present in the language to infer.

            sigma (str): An iterable of chars, represents the alphabet.

            red_states (set): An iterable of strings, should remain default
                to run Gold algorithm.

        Raises:
            A ``RuntimeError`` exception if the input data is not consistent.
        """
        # Check that all strings have their letters in sigma
        for str_set in [s_plus, s_minus, red_states]:
            for string in str_set:
                if any(char not in sigma for char in string):
                    raise RuntimeError(
                        "Some characters are in the samples, "
                        "but not in the alphabet"
                    )

        # Check that the red states are prefix closed
        if not is_prefix_closed(red_states):
            raise RuntimeError(
                "The set of red states must be prefix-closed."
            )

        # Check that s_plus and s_minus are disjoint
        if (
            any(string in s_plus for string in s_minus) or
            any(string in s_minus for string in s_plus)
        ):
            raise RuntimeError(
                "S+ and S- must not overlap"
            )

    def get_value_from_sample(self, w: str) -> int:
        """
        Returns the value used to fill this :py:class:`GoldObservationTable`
        for a given word.

        Args:
            w (str): An arbitray word.

        Returns:
            - :py:attr:`ONE` if ``w`` is in :py:attr:`self.s_plus`,
            - :py:attr:`ZERO` if it is in :py:attr:`s_minus`,
            - :py:attr:`STAR` otherwise
        """
        return (
            GoldObservationTable.ONE  if w in self.s_plus  else
            GoldObservationTable.ZERO if w in self.s_minus else
            GoldObservationTable.STAR
        )

    @staticmethod
    def are_obviously_different(row1: list, row2: list) -> bool:
        """
        Checks whether two rows are obviously different.

        Args:
            row1 (list): A row of this :py:class:`GoldObservationTable`.
            row2 (list): A row of this :py:class:`GoldObservationTable`.

        Returns:
            ``True`` iff one of these two row contains at least one ``ONE``
            and the other row contains at least one ZERO at a given index.
        """
        return any(
            (
                v1 == GoldObservationTable.ONE and
                v2 == GoldObservationTable.ZERO
            ) or (
                v1 == GoldObservationTable.ZERO and
                v2 == GoldObservationTable.ONE
            )
            for (v1, v2) in zip(row1, row2)
        )

    def choose_obviously_different_blue_state(self) -> int:
        """
        Finds a blue state (row) that is obviously different from all the
        red states.

        Returns:
            A state (if found), ``None`` otherwise.
        """
        blue_candidates = [
            blue_state
            for (blue_state, blue_state_val) in self.blue_states.items()
            if all(
                GoldObservationTable.are_obviously_different(blue_state_val, red_state_val)
                for red_state_val in self.red_states.values()
            )
        ]
        if not blue_candidates:
            return None
        else:
            return self.blue_state_choice_func(blue_candidates)

    def try_and_promote_blue(self) -> bool:
        """
        Tries to find a blue state to promote (cf Gold algorithm).
        If such a state is found, the function promotes it and updates this
        :py:class:`GoldObservationTable` accordingly.

        Returns:
            ``True`` iff a state has been promoted, ``False`` otherwise.
        """
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
        """
        Finds a red state that is compatible according to a row.

        Args:
            row (list): A vector of values in ``{ONE, ZERO, STAR}``,
                corresponding to a blue state.

        Returns:
            A red state that is compatible (not obviously different)
        """
        candidates = [
            red_state
            for (red_state, red_state_val) in self.red_states.items()
            if not GoldObservationTable.are_obviously_different(row, red_state_val)
        ]
        if not candidates:
            return None
        return self.red_state_choice_func(candidates)

    def try_and_fill_holes(self):
        """
        Tries to fill all the holes (:py:attr:`STAR`) that are in the observation
        table after the promoting phase.

        Returns:
             ``True`` if it succeeds, ``False`` otherwise.
        """
        if not self.fill_holes:
            return True

        for (blue_state, blue_state_val) in self.blue_states.items():
            red_state = self.choose_compatible_red_state(blue_state_val)
            if red_state is None:  # This should never happen
                return False
            red_state_val = self.red_states[red_state]
            self.red_states[red_state] = [
                red_state_val[i] if red_state_val[i] != GoldObservationTable.STAR else
                blue_state_val[i]
                for i in range(self.row_length)
            ]

        self.red_states = {
            red_state: [
                GoldObservationTable.ONE if red_state_val[i] != GoldObservationTable.ZERO else
                GoldObservationTable.ZERO
                for i in range(self.row_length)
            ] for red_state, red_state_val in self.red_states.items()
        }

        for (blue_state, blue_state_val) in self.blue_states.items():
            red_state = self.choose_compatible_red_state(blue_state_val)
            if red_state is None:
                return False
            self.blue_states[blue_state] = [
                blue_state_val[i] if blue_state_val[i] != self.STAR
                else self.red_states[red_state][i]
                for i in range(self.row_length)
            ]
        return True

    def to_automaton(self) -> tuple:
        """
        Builds an automaton from the observation table information.

        Returns:
            A tuple ``(g, success)`` where: ``g`` is the inferred
            :py:class:`pybgl.Automaton`;
            ``success`` equals ``True`` iff the algorithm succeeded in building
            an automaton.
            If ``False``, ``g`` is the Prefix Tree Acceptor (PTA) accepting ``s_plus``.
        """
        if self.fill_holes:
            if not self.try_and_fill_holes():
                return False, self.make_pta()
        epsilon_idx = self.exp.index("")
        states = sorted(list(self.red_states.keys()), key=lambda s: (len(s), s))

        transitions = []
        if self.fill_holes:
            for q in states:
                for a in self.sigma:
                    qa_val = self.red_states.get(
                        q + a,
                        self.blue_states.get(q + a, None)
                    )
                    for (r, r_val) in self.red_states.items():
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
        final_states = defaultdict(
            bool,
            {
                states.index(state): (self.red_states[state][epsilon_idx] == self.ONE)
                for state in states
            }
        )
        g = make_automaton(
            transitions,
            states.index(""),
            make_assoc_property_map(final_states)
        )

        if not self.fill_holes:
            if not self.is_consistent_with_samples(g):
                return (self.make_pta(), False)

        return (g, True)

    def make_pta(self) -> Trie:
        """
        Builds the PTA (Prefix Tree Acceptor) corresponding to the positive
        examples related to this :py:class:`GoldObservationTable` instance.

        Returns:
            The corresponding :py:class:`pybgl.Trie` instance.
        """
        g = Trie()
        for s in self.s_plus:
            g.insert(s)
        return g

    def is_consistent_with_samples(self, g: Automaton) -> bool:
        """
        Checks if a given automaton complies with the positive and negative
        examples.

        _Remarks:_

        - Using the :py:class:`pybgl.Automaton` implementation, this method
          always returns ``True``.
        - If the automaton class supports rejecting states,
          :py:meth:`GoldObservationTable.is_consistent_with_samples` should be
          overloaded and check whether ``g`` is consistent
          with :py:attr:`self.s_plus` (positive examples) and
          with :py:attr:`self.s_minus` (negative examples).

        Args:
            g (Automaton): An automaton instance.

        Returns:
            ``True`` if ``g`` accepts the positive examples and rejects the negative
            examples, ``False`` otherwise.
        """
        return True

    def to_html(self) -> str:
        """
        Exports to HTML this :py:class:`GoldObservationTable` instance.

        Returns:
            The corresponding HTML string.
        """
        def str_to_html(s: str) -> str:
            return repr(s) if s else "&#x3b5;"

        def str_to_red_html(s: str) -> str:
            return "<font color='red'>%s</font>" % str_to_html(s)

        def str_to_blue_html(s: str) -> str:
            return "<font color='blue'>%s</font>" % str_to_html(s)

        return "<table>{header}{rows}</table>".format(
            header="<tr><th></th>%s</tr>" % (
                "".join(
                    "<td>%s</td>" % str_to_html(suffix)
                    for suffix in self.exp
                )
            ),
            rows="".join(
                "<tr><th>{prefix}</th>{values}</tr>".format(
                    prefix=str_to_red_html(red_state),
                    values="".join(
                        "<td>%s</td>" % self.red_states[red_state][i]
                        for i in range(self.row_length)
                    )
                ) for red_state in self.red_states
            ) + "".join(
                "<tr><th>{prefix}</th>{values}</tr>".format(
                    prefix=str_to_blue_html(blue_state),
                    values=''.join(
                        "<td>%s</td>" % self.blue_states[blue_state][i]
                        for i in range(self.row_length)
                    )
                ) for blue_state in self.blue_states
            )
        )
