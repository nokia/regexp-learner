# regexp-learner

[![PyPI](https://img.shields.io/pypi/v/regexp_learner.svg)](https://pypi.python.org/pypi/regexp_learner/)
[![Build](https://github.com/nokia/regexp-learner/workflows/build/badge.svg)](https://github.com/nokia/regexp-learner/actions/workflows/build.yml)
[![Documentation](https://github.com/nokia/regexp-learner/workflows/docs/badge.svg)](https://github.com/nokia/regexp-learner/actions/workflows/docs.yml)
[![ReadTheDocs](https://readthedocs.org/projects/regexp-learner/badge/?version=latest)](https://regexp-learner.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/nokia/regexp-learner/branch/master/graph/badge.svg?token=OZM4J0Y2VL)](https://codecov.io/gh/nokia/regexp-learner)

## Overview

[regexp-learner](https://github.com/nokia/regexp-learner) is a [Python 3](http://python.org/) module providing the following algorithms:
* __Angluin (1987):__ the L* algorithm is presented in _Learning regular sets from queries and couterexamples_, Dana Angluin, 1987 [[pdf](https://people.eecs.berkeley.edu/~dawnsong/teaching/s10/papers/angluin87.pdf)].
* __Gold (1978):__ the Gold algorithm is presented in _Complexity of automaton identification from given data_, E. Mark Gold, 1987 [[pdf](http://sebastian.doc.gold.ac.uk/papers/Language_Learning/gold78complexity.pdf)].

This module is built on top of:
* [numpy](https://pypi.org/project/numpy/);
* [pybgl](https://pypi.org/project/pybgl/), a lightweight graph library.

A [jupyter notebook](https://pypi.org/project/jupyter/) is also provided test the algorithm. Note that the [graphviz](https://pypi.org/project/jupyter/) runnables (e.g., `dot`) is required to display the automata.

## Usage

* Install [Jupyter Notebook](https://pypi.org/project/jupyter/) or [Jupyter lab](https://pypi.org/project/jupyterlab/).
* Follow [installation steps](https://github.com/nokia/regexp-learner/wiki/Installation).
* Run `jupyter notebook` or `jupyter lab`.
* Open the desired notebook.
* Run the cells.


## Links

* [Installation](https://github.com/nokia/regexp-learner/wiki/Installation)
* [Tests](https://github.com/nokia/regexp-leader/wiki/Test)

## License

This project is licensed under the [BSD-3-Clause license](https://github.com/nokia/regexp-learner/blob/master/LICENSE).
