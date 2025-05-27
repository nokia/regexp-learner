#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of the regexp-learner project
# https://github.com/nokia/regexp-learner

from collections import deque
from pybgl import (
    Automaton,
    html,
)


def automaton_match(
    g1: Automaton,
    g2: Automaton,
    verbose: bool = False
) -> str:
    """
    Tests whether two minimized deterministic ``Automaton`` recognize
    the same language. One can minimize an Automaton using
    ``pybgl.hopcroft_minimize.hopcroft_minimize``.

    Args:
        g1 (Automaton): A minimal deterministic ``Automaton`` instance.
        g2 (Automaton): A minimal deterministic ``Automaton`` instance.
        verbose (bool): Pass ``True`` to print useful HTML information.

    Returns:
        ``None`` if g1 matches g2, otherwise a counter-example (possibly
        the empty word).
    """
    def quiet(s):
        pass
    log = html if verbose else quiet
    q01 = g1.initial()
    q02 = g2.initial()
    if g1.is_final(q01) != g2.is_final(q02):
        # Contradiction for the empty word.
        return ""
    map_q1_q2 = {q01: q02}
    stack = deque()
    stack.appendleft(("", q01))

    i = 0
    while stack:
        i += 1
        log(f"<b>Iteration {i}</b>: {stack=}")
        # if i > 100:
        #     raise Exception("Infinite loop?")
        (w, q1) = stack.pop()
        q2 = map_q1_q2[q1]
        sigma1 = set(g1.sigma(q1))
        sigma2 = set(g2.sigma(q2))
        log(f"{sigma1=} {sigma2=}")
        if sigma1 == sigma2:
            for a in sigma1:
                r1 = g1.delta(q1, a)
                r2 = g2.delta(q2, a)
                log("a = %s r1 = %s r2 = %s" % (a, r1, r2))
                if map_q1_q2.get(r1) is None:
                    map_q1_q2[r1] = r2
                    stack.appendleft((w + a, r1))
                elif map_q1_q2.get(r1) == r2:
                    log("continue")
                    continue  # r1 has already been processed
                if g1.is_final(r1) != g2.is_final(r2):
                    # Contradiction
                    log("contradiction: {w=} + {a=}")
                    return w + a
        else:
            contradiction = w + sorted(
                (sigma1 - sigma2) |
                (sigma2 - sigma1)
            )[0]
            log(f"{contradiction=}")
            return contradiction
    return None
