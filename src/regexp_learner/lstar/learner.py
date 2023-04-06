#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of the regexp-learner project
# https://github.com/nokia/regexp-learner

import numpy as np
from pybgl.automaton       import Automaton, is_final, make_automaton, vertices
from pybgl.graphviz        import dotstr_to_html
from pybgl.property_map    import make_func_property_map
from pybgl.html            import html
from .observation_table    import LstarObservationTable
from .teacher              import Teacher

def make_automaton_from_observation_table(
    o: LstarObservationTable,
    verbose: bool = False
) -> Automaton:
    """
    Builds an :py:class:`Automaton` instance from an
    :py:class:`.LstarObservationTable` instance.

    Args:
        o (LstarObservationTable): An :py:class:`.LstarObservationTable` instance.
        verbose (bool); Pass ``True`` to print useful HTML information.

    Returns:
        The resulting `Automaton` instance.
    """
    def quiet(s):
        pass
    log = html if verbose else quiet
    map_row_state = dict()
    q0 = 0
    final_states = set()
    transitions = list()

    # Build states
    q = 0
    for s in sorted(o.s): # Hence q0 = 0
        row = o.row(s)
        if row not in map_row_state.keys():
            map_row_state[row] = q
            is_final = o.get(s, "")
            if is_final:
                final_states.add(q)
            log("Adding state %d for prefix %s (row = %s, is_final = %s)" % (
                q, s, o.row(s), is_final
            ))
            q += 1

    # Build transitions
    for (row, q) in map_row_state.items():
        # Find prefix leading to q
        s = None
        for s in o.s:
            if o.row(s) == row: break
        assert s is not None

        for a in o.a:
            r = map_row_state[o.row(s + a)]
            transitions.append((q, r, a))
            log("Adding %s-transition from %d (%s) to %d (%s)" % (
                a, q, o.row(s), r, o.row(s + a))
            )

    g = make_automaton(transitions, q0, make_func_property_map(lambda q: q in final_states))
    log("final_states = %s" % final_states)
    log("<pre>make_automaton_from_observation_table</pre> returns:")
    log(dotstr_to_html(g.to_dot()))
    return g

class Learner:
    """
    The learner (in the Angluin framework).
    """
    def __init__(self, teacher: Teacher, epsilon: str = "", verbose: bool = True):
        """
        Constructor.

        Args:
            teacher (Teacher): The teacher aka oracle (in the Angluin framework).
            epsilon (str): The empty word.
            verbose (bool); Pass ``True`` to print useful HTML information.
        """
        def quiet(s):
            pass
        self.teacher = teacher
        self.sigma = self.teacher.alphabet
        self.o = LstarObservationTable(self.sigma)
        self.epsilon = epsilon
        self.log = html if verbose else quiet

    def initialize(self, verbose: bool = True):
        """
        Initializes the :py:class:`.LstarObservationTable` of this :py:class:`.Learner`.

        Args:
            verbose (bool): Pass ``True`` to print useful HTML information.
        """
        self.o.s.add(self.epsilon)
        self.o.set(
            self.epsilon,
            self.epsilon,
            self.teacher.membership_query(self.epsilon)
        )
        self.extend()
        if verbose:
            self.log("<b>initialize</b>")
            self.log(self.o.to_html())

    def extend(self):
        """
        Extends the :py:class:`.LstarObservationTable` of this :py:class:`.Learner`.
        This method is triggered when the Teacher returns a counter example.
        """
        for s in {s for s in self.o.s} | {s + a for s in self.o.s for a in self.o.a}:
            for e in self.o.e:
                if self.o.get(s, e) is not None:
                    continue
                self.o.set(s, e, self.teacher.membership_query(s + e))

    def learn(self, verbose: bool = False) -> Automaton:
        """
        Trains the :py:class:`.Learner` to infer the :py:class:`Automaton`
        of the :py:class:`.Teacher`.

        Args:
            verbose (bool): Pass ``True`` to print useful HTML information.

        Returns:
            The inferred :py:class:`Automaton` instance.
        """
        self.initialize(verbose = verbose)
        i = 0
        while(True):
            if verbose:
                self.log("<b>iteration %d</b>" % (i + 1))
            is_consistent = self.o.is_consistent()
            is_closed = self.o.is_closed()
            i = 0
            while not (is_consistent and is_closed):
                if not is_consistent:
                    (s1, s2, a, e) = self.o.find_mismatch_consistency()
                    if verbose:
                        self.log(self.o.to_html())
                        self.log(
                            "The observation table is not consistent: (s1, s2, a, e) = %s, adding %s to E" % (
                                (s1, s2, a, e),
                                a + e
                            )
                        )
                    self.o.add_suffix(a + e)
                if not is_closed:
                    (s1, a) = self.o.find_mismatch_closeness()
                    if verbose:
                        self.log(self.o.to_html())
                        self.log(
                            "The observation table is not closed: (s1, a) = %s, adding s1 + a = %s to S" % (
                                (s1, a),
                                s1 + a
                            )
                        )
                    self.o.s.add(s1 + a)
                    self.o.add_prefix(s1 + a)
                self.extend()
                is_consistent = self.o.is_consistent()
                is_closed = self.o.is_closed()
                i += 1
                #if i > 10:
                #    raise Exception("Implementation error? (infinite loop)")
            if verbose:
                self.log("The observation table is closed and consistent")
                self.log(
                    """
                    <table>
                        <tr>
                            <th>Teacher</th>
                            <th>Observation table</th>
                        </tr>
                        <tr>
                            <td>%s</td>
                            <td>%s</td>
                        </tr>
                    </table>
                    """ % (
                        dotstr_to_html(self.teacher.g.to_dot()),
                        self.o.to_html()
                    )
                )
                assert self.o.is_consistent()
                assert self.o.is_closed()

            h = make_automaton_from_observation_table(self.o, verbose=False)
            if verbose:
                html(dotstr_to_html(h.to_dot()))
                html("Final states: %s" % {q for q in vertices(h) if is_final(q, h)})
            t = self.teacher.conjecture(h)
            if t is not None:
                prefixes = {t[:i] for i in np.arange(1, len(t) + 1)}
                self.o.s |= prefixes
                for s in prefixes:
                    self.o.add_prefix(s)
                self.extend()
                if verbose:
                    self.log("The teacher disagreed: t = %r" % t)
                    self.log("The following prefixes have been added to S: %s" % prefixes)
                    self.log("S is now equal to %s" % self.o.s)
                    self.log(self.o.to_html())
            else:
                if verbose and t is not None:
                    self.log("The teacher agreed :-)")
                break
            i += 1
        return make_automaton_from_observation_table(self.o)
