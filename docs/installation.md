# Installation
## Linux (Debian / Ubuntu)

* Install the needed dependencies:

```bash
sudo apt update
sudo apt install git graphviz python3 python3-notebook python3-numpy python3-pytest
```

* If you are developer, please also install the following packages:

```bash
sudo apt install python3-pip bumpversion python3-coverage python3-pytest python3-pytest-cov python3-pytest-runner python3-sphinx python3-sphinx-rtd-theme
sudo pip3 install sphinx_mdinclude
```

_Note:_ In modern Debians, ``pip3`` system-wide installation is no more possible. You must either use a virtual environment or either install ``sphinx_mdinclude`` as follows:

```bash
sudo pip3 install sphinx_mdinclude --break-system-packages
```

## Windows

* Install [anaconda](https://www.anaconda.com/products/distribution) and run:

```bash
pip install -r requirements.txt
pip install -r requirements_dev.txt
```

## Common steps

* Clone the repository and install the package.

```bash
git clone https://github.com/nokia/regexp-learner.git
cd regexp-learner 
python3 setup.py install
```
