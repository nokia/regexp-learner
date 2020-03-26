#!/usr/bin/env pytest-3
# -*- coding: utf-8 -*-

__author__     = "Marc-Olivier Buob"
__maintainer__ = "Marc-Olivier Buob"
__email__      = "marc-olivier.buob@nokia-bell-labs.com"
__copyright__  = "Copyright (C) 2018, Nokia"
__license__    = "BSD-3"

from pybgl.automaton            import Automaton, is_complete, make_automaton
from pybgl.graphviz             import dotstr_to_html
from pybgl.html                 import html
from pybgl.property_map         import make_func_property_map
from lstar.automaton_match      import automaton_match
from lstar.observation_table    import ObservationTable
from lstar.learner              import Learner, make_automaton_from_observation_table
from lstar.teacher              import Teacher

G1 = make_automaton(
    [
        (0, 0, 'a'), (0, 1, 'b'),
        (1, 2, 'a'), (1, 1, 'b'),
        (2, 1, 'a'), (2, 1, 'b'),
    ], 0,
    make_func_property_map(lambda q: q == 1)
)

G2 = make_automaton(
    [
        (0, 0, 'a'), (0, 1, 'b'),
    ], 0,
    make_func_property_map(lambda q: q == 1)
)

G3 = make_automaton(
    [
        (0, 0, 'a'), (0, 1, 'b'),
    ], 0,
    make_func_property_map(lambda q: False)
)

G4 = make_automaton(
    [
        (0, 0, 'a'), (0, 1, 'b'),
        (1, 1, 'b'), (1, 0, 'a')
    ], 0,
    make_func_property_map(lambda q: q == 1)
)

G5 = make_automaton(
    [
        (0, 0, 'a'), (0, 1, 'b'),
        (1, 1, 'b'), (1, 0, 'a')
    ], 0,
    make_func_property_map(lambda q: False)
)

def test_make_automaton_from_observation_table():
    # Build observation table
    o = ObservationTable("ab")
    o.s = {"", "b", "ba"}
    o.set("",    "", False); o.set("",    "a", False)
    o.set("b",   "", True) ; o.set("b",   "a", False)
    o.set("a",   "", False); o.set("a",   "a", False)
    o.set("ba",  "", False); o.set("ba",  "a", True)
    o.set("bb",  "", True) ; o.set("bb",  "a", False)
    o.set("baa", "", True) ; o.set("baa", "a", False)
    o.set("bab", "", True) ; o.set("bab", "a", False)
    is_consistent = o.is_consistent()
    is_closed = o.is_closed()

    # Check
    html(o.to_html())
    html("This observation table is %sconsistent" % ("" if is_consistent else "<b>not</b> "))
    html("This observation table is %sclosed"   % ("" if is_closed   else "<b>not</b> "))
    assert is_consistent
    assert is_closed

    # Build and display corresponding automatonbb
    h = make_automaton_from_observation_table(o)

    html("<b>obtained</b>")
    html(dotstr_to_html(h.to_dot()))
    html("<b>expected</b>")
    html(dotstr_to_html(G1.to_dot()))
    assert automaton_match(G1, h) == None

def test_make_automaton_from_observation_table2():
    # Build observation table
    o = ObservationTable("ab")
    o.s = {"", "a"}
    o.set("", "", False)
    o.set("a", "", True)
    o.set("b", "", False)
    o.set("aa", "", True)
    o.set("ab", "", False)
    is_consistent = o.is_consistent()
    is_closed = o.is_closed()

    # Check
    html(o.to_html())
    html("This observation table is %sconsistent" % ("" if is_consistent else "<b>not</b> "))
    html("This observation table is %sclosed"   % ("" if is_closed   else "<b>not</b> "))
    assert is_consistent
    assert is_closed

    # Build and display corresponding automatonbb
    h = make_automaton_from_observation_table(o)
    expected = make_automaton(
        [
            (0, 0, 'b'), (0, 1, 'a'),
            (1, 1, 'a'), (1, 0, 'b')
        ], 0,
        make_func_property_map(lambda q: q == 1)
    )
    html("<b>obtained</b>")
    html(dotstr_to_html(h.to_dot()))
    html("<b>expected</b>")
    html(dotstr_to_html(expected.to_dot()))
    assert automaton_match(expected, h) == None

def test_learners(gs = [G1, G2, G3, G4, G5], verbose = False):
    def test_learner(g :Automaton, verbose :bool = False, write_files :bool = False):
        if not is_complete(g):
            html(dotstr_to_html(g.to_dot()))
            html("Ignored, this automaton must be finite, deterministic and complete")
            return

        teacher = Teacher(g)
        html("<b>Teacher</b>")
        html(dotstr_to_html(teacher.g.to_dot()))

        learner = Learner(teacher)
        h = learner.learn(verbose = verbose, write_files = write_files)
        html("<b>Learner</b>")
        html(dotstr_to_html(h.to_dot()))

        assert automaton_match(g, h) == None
        html(":-)")

    for (i, g) in enumerate(gs):
        html("<h3>Test G%d</h3>" % (i + 1))
        test_learner(g, verbose)
