SHELL:=/bin/bash

# ~~~~~ Python and nextflow installation ~~~~~~ #
UNAME:=$(shell uname)
PATH:=$(CURDIR)/conda/bin:$(PATH)
unexport PYTHONPATH
unexport PYTHONHOME

ifeq ($(UNAME), Darwin)
CONDASH:=Miniconda3-4.5.4-MacOSX-x86_64.sh
endif

ifeq ($(UNAME), Linux)
CONDASH:=Miniconda3-4.5.4-Linux-x86_64.sh
endif

CONDAURL:=https://repo.continuum.io/miniconda/$(CONDASH)

conda:
	@echo ">>> Setting up conda..."
	@wget "$(CONDAURL)" && \
	bash "$(CONDASH)" -b -p conda && \
	rm -f "$(CONDASH)"

# curl -s https://get.nextflow.io | bash
install: conda
	conda install -y \
	bioconda::nextflow=19.10.0 \
	anaconda::flask=1.1.1

test:
	nextflow -version
	which nextflow
	which python
	python -c 'import flask; print(flask.__version__)'

# ~~~~~ Run ~~~~~ #
export FLASK_APP:=server.py
export FLASK_RUN_PORT:=5000
export FLASK_RUN_HOST:=127.0.0.1
server:
	flask run

bash:
	bash

export NXF_ANSI_LOG:=false
run: clean
	nextflow run main.nf -with-weblog http://$(FLASK_RUN_HOST):$(FLASK_RUN_PORT)/

clean:
	rm -f trace.txt* report.html* .nextflow.log* timeline.html*
