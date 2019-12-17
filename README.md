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

The Nextflow pipeline will run through a set of simple processes like this:

```
$ make run
rm -f trace.txt* report.html* .nextflow.log* timeline.html*
nextflow run main.nf -with-weblog http://127.0.0.1:5000/
N E X T F L O W  ~  version 19.10.0
Launching `main.nf` [clever_snyder] - revision: 02edc0e59b
* Project dir:        /home/nextflow-communicator
* Launch dir:         /home/nextflow-communicator
* Work dir:           /home/nextflow-communicator/work
[44/e61207] Submitted process > make_file (3)
[ed/5a6ca2] Submitted process > make_file (2)
[fe/cc0c60] Submitted process > make_file (1)
```

Each Nextflow process will create a small `communicator.json` file in its working directory containing custom information saved with the `record.py` script (`bin/record.py`).

Meanwhile, Nextflow's http web-log functionality will send POST messages to the Flask server, where the messages will be parsed and the `communicator.json` files will be detected, allowing the data to be loaded and combined with the standard Nextflow task 'trace' metadata:

```

process: make_file (make_file (1))
trace: {'task_id': 1, 'status': 'COMPLETED', 'hash': 'fe/cc0c60', 'name': 'make_file (1)', 'exit': 0, 'submit': 1576602495503, 'start': 1576602495602, 'process': 'make_file', 'tag': None, 'module': [], 'container': None, 'attempt': 1, 'script': '\n    touch "1.txt"\n    record.py --key "input_val" --value "1" --type "val"\n    record.py --key "output_file" --value "1.txt" --type "file"\n    ', 'scratch': None, 'workdir': '/home/nextflow-communicator/work/fe/cc0c602950022594390ba096b8dea9', 'queue': None, 'cpus': 1, 'memory': None, 'disk': None, 'time': None, 'env': 'PATH=/home/nextflow-communicator/bin:$PATH\n', 'error_action': None, 'complete': 1576602497502, 'duration': 1999, 'realtime': 1900, 'native_id': 30651}
workdir: /home/nextflow-communicator/work/fe/cc0c602950022594390ba096b8dea9
communicator_data: {'input_val': '1', 'output_file': '/home/nextflow-communicator/work/fe/cc0c602950022594390ba096b8dea9/1.txt'}

```

# Software

- Nextflow

- Python 3

- Flask

- GNU `make` and `bash` for Makefile wrapper recipes
