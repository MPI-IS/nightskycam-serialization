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

## Poetry

This package uses [poetry](https://python-poetry.org/).
