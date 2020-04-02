#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
#This file is part of veggie
#Copyright © 2018 Nokia Corporation and/or its subsidiary(-ies). All rights reserved. *
#
#Contact:
#    Marc-Olivier Buob <marc-olivier.buob@nokia-bell-labs.com>
#    Anne Bouillard    <anne.bouillard@nokia-bell-labs.com>
#    Achille Salaün    <achille.salaun@nokia.com>
#
#This software, including documentation, is protected by copyright controlled by Nokia Corporation. All rights are reserved. Copying, including reproducing, storing, adapting or translating, any or all of this material requires the prior written consent of Nokia Corporation. This material also contains confidential information which may not be disclosed to others * without the prior written consent of Nokia.
#
# Usage:
#     python3 setup.py install
#     python3 setup.py bdist_rpm
#

from setuptools import find_packages, setup

__version__ = (0, 9, 2)

README = ""
try:
    with open("README.rst") as f_readme:
        README = f_readme.read()
except:
    pass

HISTORY = ""
try:
    with open("HISTORY.rst") as f_history:
        HISTORY = f_history.read()
except:
    pass

LONG_DESCRIPTION = "%s\n\n%s" % (README, HISTORY)

# Copy is only triggered if the file does not yet exists.

setup(
    name             = "regexp_learner",
    version          = ".".join(["%s" % x for x in __version__]),
    description      = "regexp_learner",
    long_description = LONG_DESCRIPTION,
    author           = "Marc-Olivier Buob",
    author_email     = "marc-olivier.buob@nokia-bell-labs.com",
    #url              = "http://github.com/nokia/veggie",
    license          = "BSD-3",
    zip_safe         = False,
    packages         = find_packages(),
    package_dir      = {"regexp_learner" : "regexp_learner/"},
    requires         = ["typing"],
    test_suite       = "tests",
)
