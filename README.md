# Taxonomy API

## Setup
Tested using Python 3.7.  Use
```bash
pip install -r requirements.txt
```
if you just want to run the web service, or
```bash
pip install -r test_requirements.txt
```
if you want to run tests.

## Load database

Script to load data from SQL files:
```bash
python load_db.py --projects=data/projects.sql --taxonomies=data/taxonomies.sql
```

I've omitted the data files from the public repo, update filenames as needed.
Of course the API could also be extended with POST endpoints to add data,
but as I was provided with SQL snippets, I just batch loaded those directly.

## Run web service

To run locally port 7799, use
```bash
python app.py
```

This exposes the following endpoints:
* `/studies` – get all studies
* `/studies?taxonomy_common_name=<common name>` – filter studies by taxonomy common name
* `/study/<project id>` – get details for a single study by id

Ideally there would be some Swagger docs, but hopefully this is pretty self-explanatory!

## Run tests

```bash
python -m pytest
```
