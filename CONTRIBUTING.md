Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report bugs

Report bugs [here](https://gitlabe2.ext.net.nokia.com/mandrews/hockeytracking/-/issues)

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitLab issues for bugs. Anything tagged with _"Bug"_ and _"Help
wanted"_ is open to whoever wants to implement it.

### Implement Features

Look through the GitLab issues for features. Anything tagged with _"Enhancement"_
and _"Help wanted"_ is open to whoever wants to implement it.

### Write Documentation

Pattern clustering could always use more documentation, whether as part of the
official Pattern clustering docs, in docstrings, or even on the web in blog posts,
articles, and such.

### Submit Feedback

The best way to send feedback is to [file an issue](https://gitlabe2.ext.net.nokia.com/mandrews/hockeytracking).

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

## Get started!

Ready to contribute? Here's how to set up the package for local development.

1. Fork the repo.
2. Clone your fork locally:

```bash
git clone git@github.com:your_name_here/pattern-clustering.git
```

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development:

```bash
mkvirtualenv regexp-learner 
cd regexp-learner/
python setup.py develop
```

4. Install  `flake8` and `tox` in you virtualenv:

```bash
pip install flake8 tox
```

5. Create a branch for local development to make your changes locally:

```bash
git checkout -b name-of-your-bugfix-or-feature
```

6. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox:

```bash
flake8 regexp-learner tests
python setup.py test or pytest
tox
```

7. Commit your changes and push your branch to GitLab:

```bash
git add .
git commit -m "Your detailed description of your changes."
git push origin name-of-your-bugfix-or-feature
```

7. Submit a pull request through the GitLab website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python >=3.6. Check
   https://gitlabe2.ext.net.nokia.com/mandrews/hockeytracking/-/pipelines
   and make sure that the tests pass for all supported Python versions.

## Tips

To run a subset of tests:

```bash
pytest tests.test_foo
```

## Deploying

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in `HISTORY.md`).
Then run:

```bash
bump2version patch # possible: major / minor / patch
git push
git push --tags
```

GitLab will then deploy to PyPI if tests pass.
