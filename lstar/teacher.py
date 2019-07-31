#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__     = "Marc-Olivier Buob"
__maintainer__ = "Marc-Olivier Buob"
__email__      = "marc-olivier.buob@nokia-bell-labs.com"
__copyright__  = "Copyright (C) 2018, Nokia"
__license__    = "BSD-3"

from pybgl.automaton        import Automaton, accepts, alphabet, is_complete, is_finite
from lstar.automaton_match  import automaton_match

class Teacher:
    def __init__(self, g :Automaton):
        assert is_complete(g)
        assert is_finite(g)
        #assert is_minimal(g) # Not implemented
        self.g = g

    @property
    def alphabet(self) -> set:
        return alphabet(self.g)

    def conjecture(self, h :Automaton) -> str:
        return automaton_match(self.g, h)

    def membership_query(self, w :str) -> bool:
        return accepts(w, self.g)
