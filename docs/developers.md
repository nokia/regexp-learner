# Developer's corner 
## Tests

To launch the test suite, run:
* If the package is installed system-wide:

```bash
pytest
```

* Else, with `poetry`:

```bash
poetry install --with test
poetry run coverage run -m pytest
poetry run coverage xml
```

* Else, with `tox`:
  * The versions of python that are tested are listed in `tox.ini`.
  * To run the tests, run:

```bash
tox -e py
```

## Documentation

To build the documentation, run:
* If the package is installed system-wide and if `make` is installed:

```bash
make docs
```

* Otherwise:

```bash
poetry run sphinx-apidoc -f -o docs/ src/
poetry run sphinx-build -b html docs/ docs/_build
```

## Publish a release

1. Update the changelog `HISTORY.md`, then add and commit this change:

```bash
git add README.md
git commit -m "Updated README.md"
```

2. Increase the version number using `bumpversion`:

```bash
bumpversion patch # Possible values major / minor / patch
git push
git push --tags
```
