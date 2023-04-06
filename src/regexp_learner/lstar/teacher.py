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
    The :py:class:`Teacher` class (aka oracle) in the Angluin framework.
    """

    def __init__(self, g: Automaton):
        """
        Constructor.

        Args:
            g: The :py:class:`pybgl.Automaton` that the :py:class:`Learner` tries to infer.
        """
        assert is_complete(g)
        assert is_finite(g)
        #assert is_minimal(g) # Not implemented
        self.g = g

    @property
    def alphabet(self) -> set:
        """
        Accessor the alphabet of this :py:class:`Teacher` instance.

        Returns:
            The alphabet of the :py:class:`pybgl.Automaton` of this
            :py:class:`Teacher` instance.
        """
        return alphabet(self.g)

    def conjecture(self, h :Automaton) -> str:
        """
        Handles a conjecture query.
        (see Angluin's paper or `Angluin.pdf <https://github.com/nokia/regexp-learner/blob/master/Angluin.pdf>`__ in this repository).

        Args:
            h (Automaton): The tested :py:class:`pybgl.Automaton`
                (typically, submitted by the :py:class:`Learner`).

        Returns:
            ``True`` if ``h`` matches the ``Automaton`` of this :py:class:`Teacher`
            instance, ``False`` otherwise.
        """
        return automaton_match(self.g, h)

    def membership_query(self, w :str) -> bool:
        """
        Handles a membership query.
        (see Angluin's paper or `Angluin.pdf <https://github.com/nokia/regexp-learner/blob/master/Angluin.pdf>`__ in this repository).

        Args:
            w: The tested word (typically, submitted by the :py:class:`Learner`).

        Returns:
            ``True`` if ``w`` is matched by the ``Automaton`` of this :py:class:`Teacher`
            instance, ``False`` otherwise.
        """
        return accepts(w, self.g)
