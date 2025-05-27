#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of the regexp-learner project
# https://github.com/nokia/regexp-learner

"""Top-level package."""

__author__ = "Marc-Olivier Buob, Maxime Raynal"
__maintainer__ = "Marc-Olivier Buob, Maxime Raynal"
__email__ = "marc-olivier.buob@nokia-bell-labs.com, maxime.raynal@nokia.com"
__copyright__ = "Copyright (C) 2019, Nokia"
__license__ = "BSD-3"
__version__ = '1.0.2'  # Use single quotes for bumpversion (see setup.cfg)

from .gold import (
    GoldObservationTable,
    gold,
)
from .lstar import (
    automaton_match,
    Learner,
    LstarObservationTable,
    Teacher,
    make_automaton_from_observation_table,
)
from .strings import (
    prefixes,
    is_prefix_closed,
    suffixes,
    is_suffix_closed,
)
