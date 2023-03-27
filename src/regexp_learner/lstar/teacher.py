#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__     = "Marc-Olivier Buob"
__maintainer__ = "Marc-Olivier Buob"
__email__      = "marc-olivier.buob@nokia-bell-labs.com"
__copyright__  = "Copyright (C) 2018, Nokia"
__license__    = "BSD-3"

from pybgl.automaton   import Automaton, accepts, alphabet, is_complete, is_finite
from .automaton_match  import automaton_match

class Teacher:
    """
    The ``Teacher`` class (aka oracle) in the Angluin framework.
    """

    def __init__(self, g :Automaton):
        """
        Constructor.

        Args:
            g: The ``Automaton`` that the ``Learner`` tries to infer.
        """
        assert is_complete(g)
        assert is_finite(g)
        #assert is_minimal(g) # Not implemented
        self.g = g

    @property
    def alphabet(self) -> set:
        """
        Accessor the he alphabet of this ``Teacher`` instance.

        Returns:
            The alphabet of the ``Automaton`` of this ``Teacher`` instance.
        """
        return alphabet(self.g)

    def conjecture(self, h :Automaton) -> str:
        """
        Handles a conjecture query (see Angluin framework).

        Args:
            h (Automaton): The tested ``Automaton``
                (typically, submitted by the ``Learner``).

        Returns:
            ``True`` if ``h`` matches the ``Automaton`` of this ``Teacher``
            instance, ``False`` otherwise.
        """
        return automaton_match(self.g, h)

    def membership_query(self, w :str) -> bool:
        """
        Handles a membership query (see Angluin framework).

        Args:
            w: The tested word (typically, submitted by the ``Learner``).

        Returns:
            ``True`` if ``w`` is matched by the ``Automaton`` of this ``Teacher``
            instance, ``False`` otherwise.
        """
        return accepts(w, self.g)
