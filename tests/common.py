from pybgl import (
    html as _html,
    in_ipynb,
)


def html(s):
    if in_ipynb():
        _html(s)
