# nextflow-communicator

Demo app for passing custom data out of Nextflow pipeline processes and into a logging server.

# Installation

Clone this repo:

```
git clone https://github.com/stevekm/nextflow-communicator.git
cd nextflow-communicator
```

If you do not have Nextflow, Python 3, and Flask already installed, then run the installation recipe:

```
make install
```

- This will install the dependencies required with `conda` in the current directory

# Usage

First, start the Flask server:

```
make server
```

Then, in another terminal session, run the Nextflow pipeline:

```
make run
```

# Software

- Nextflow

- Python 3

- Flask

- GNU `make` and `bash` for Makefile wrapper recipes
