#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of the regexp-learner project.
# https://github.com/nokia/regexp-learner

__author__     = "Marc-Olivier Buob"
__maintainer__ = "Marc-Olivier Buob"
__email__      = "marc-olivier.buob@nokia-bell-labs.com"
__copyright__  = "Copyright (C) 2023, Nokia"
__license__    = ""


"""The setup script."""

from setuptools     import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.md") as history_file:
    history = history_file.read()

requirements = []
setup_requirements = ["pytest-runner",]
test_requirements = ["pytest>=3",]

setup(
    author="Marc-Olivier Buob, Maxime Raynal",
    author_email="marc-olivier.buob@nokia-bell-labs.com, maxime.raynal@nokia.com",
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3"
    ],
    description="Python3 module providing some algorithms to infer automata and regular expressions.",
    entry_points={
        "console_scripts": [
        ],
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/x-md",
    include_package_data=True,
    keywords="Language theory, grammar inference",
    name="regexp_learner",
    packages=find_packages("src"),
    package_dir={"": "src"},
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/nokia/regexp-learner/",
    version='0.2.0', # Use single quotes, see https://github.com/oceanprotocol/ocean.py/issues/194
    zip_safe=False,
)
