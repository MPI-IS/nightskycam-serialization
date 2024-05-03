[![Python package](https://github.com/MPI-IS/nightskycam-serialization/actions/workflows/tests.yml/badge.svg)](https://github.com/MPI-IS/nightskycam-serialization/actions/workflows/tests.yml)
[![PyPI version](https://img.shields.io/pypi/v/nightskycam-serialization.svg)](https://pypi.org/project/nightskycam-serialization/)


> 🚧 **Under Construction**  
> This project is currently under development. Please check back later for updates.


# Nightskycam Serialization

## About

This is is a support package for:

- [nightskycam](https://gitlab.is.tue.mpg.de/allsky/nightskycam)
- [nightskycam-server](https://gitlab.is.tue.mpg.de/allsky/nightskycam-server)

These two packages do not depend on each other, yet the services they spawn will communicate with each other in the form of
serialized messages (sent via websockets). This requires the code in these two packages to follow the same convention on how
messages are serialized and deserialized. To enforce this, these two packages are dependant on the nightskycam-serialization
package and use its API for serializing / deserializing messages.

## Getting Started as a User (using `pip`)

Dependency management with `pip` is easier to set up than with `poetry`, but the optional dependency-groups are not installable with `pip`.

* Create and activate a new Python virtual environment:
  ```bash
  python3 -m venv --copies venv
  source venv/bin/activate
  ```
* Update `pip` and build package:
  ```bash
  pip install -U pip  # optional but always advised
  pip install .       # -e option for editable mode
  ```

## Getting Started as a Developer (using `poetry`)

Dependency management with `poetry` is required for the installation of the optional dependency-groups.

* Install [poetry](https://python-poetry.org/docs/).
* Install dependencies for package
  (also automatically creates project's virtual environment):
  ```bash
  poetry install
  ```
* Install `dev` dependency group:
  ```bash
  poetry install --with dev
  ```
* Activate project's virtual environment:
  ```bash
  poetry shell
  ```

## Tests (only possible for setup with `poetry`, not with `pip`)


To install `test` dependency group:
```bash
poetry install --with test
```

To run the tests:
```bash
python -m pytest tests
```

To extract coverage data:
* Get code coverage by measuring how much of the code is executed when running the tests:
  ```bash
  coverage run -m pytest tests
  ```
* View coverage results:
  ```bash
  # Option 1: simple report in terminal.
  coverage report
  # Option 2: nicer HTML report.
  coverage html  # Open resulting 'htmlcov/index.html' in browser.
  ```
