#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of the regexp-learner project
# https://github.com/nokia/regexp-learner

from collections        import deque
from pybgl.automaton    import Automaton, delta, initial, is_final, sigma, vertices
from pybgl.html         import html

def automaton_match(g1 :Automaton, g2 :Automaton, verbose = False) -> str:
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
    q01 = initial(g1)
    q02 = initial(g2)
    if is_final(q01, g1) != is_final(q02, g2):
        # Contradiction for the empty word.
        return ""
    map_q1_q2 = {q01 : q02}
    stack = deque()
    stack.appendleft(("", q01))

    i = 0
    while stack:
        i += 1
        log("<b>Iteration %d</b>: stack = %s" % (i, stack))
        #if i > 100:
        #    raise Exception("Infinite loop?")
        (w, q1) = stack.pop()
        q2 = map_q1_q2[q1]
        sigma1 = set(sigma(q1, g1))
        sigma2 = set(sigma(q2, g2))
        log("sigma1 = %s sigma2 = %s" % (sigma1, sigma2))
        if sigma1 == sigma2:
            for a in sigma1:
                r1 = delta(q1, a, g1)
                r2 = delta(q2, a, g2)
                log("a = %s r1 = %s r2 = %s" % (a, r1, r2))
                if map_q1_q2.get(r1) is None:
                    map_q1_q2[r1] = r2
                    stack.appendleft((w + a, r1))
                elif map_q1_q2.get(r1) == r2:
                    log("continue")
                    continue # r1 has already been processed
                if is_final(r1, g1) != is_final(r2, g2):
                    # Contradiction
                    log("contradiction: w + a = %s" % w + a)
                    return w + a
        else:
            contradiction = w + sorted((sigma1 - sigma2) | (sigma2 - sigma1))[0]
            log("contradiction: %s" % contradiction)
            return contradiction
    return None
