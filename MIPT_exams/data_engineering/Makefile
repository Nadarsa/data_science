.PHONY: all download preprocess train evaluate clean

PYTHON := python
ETL_DIR := etl

all: download preprocess train evaluate

download:
	$(PYTHON) -m $(ETL_DIR).load_data

preprocess:
	$(PYTHON) -m $(ETL_DIR).preprocess

train:
	$(PYTHON) -m $(ETL_DIR).train_model

evaluate:
	$(PYTHON) -m $(ETL_DIR).evaluate

clean:
	rm -rf logs/*.log results/*.pkl results/*.json preprocessed/*.csv
