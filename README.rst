lstar
==============

.. _pybgl: https://github.com/nokia/pybgl.git 
.. _wiki: https://github.com/nokia/regexp-learner/wiki
.. _graphviz: http://graphviz.org/
.. _Python3: http://python.org/

`lstar` is a Python3_ module implementing the L* algorithm proposed in "Learning regular sets from queries and couterexamples", Dana Angluin, 1987.

This module is built on top of numpy and pybgl_, a lightweight graph library. A jupyter notebook is also provided test the algorithm. To display automata, graphviz_ must be installed.

==================
Online demo
==================

.. _Notebook: https://github.com/nokia/regexp-learner/blob/master/Angluin.ipynb

* Open the Notebook_ in Github to see online demo.

==================
Playing with `lstar` module
==================

* Install Jupyter Notebook
* Follow Installation_ steps
* Run `jupyter-notebook` and open the `Angluin.ipynb` notebook through the web interface.
* Execute each cells to reproduce the online demo.
* Feel free to modify/add Teacher's automaton (see Test section) to see how L* algorithm proceeds.

==================
More about `lstar` module
==================

.. _Installation: https://github.com/nokia/regexp-learner/wiki/Installation
.. _Tests: https://github.com/nokia/regexp-leader/wiki/Test

- Installation_
- Tests_

=======
License
=======

This project is licensed under the BSD-3-Clause license - see the `LICENSE <https://github.com/nokia/regexp-learner/blob/master/LICENSE>`_.
