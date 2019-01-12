merge-keepass2
==============

[![Build Status](https://travis-ci.org/azeemba/merge-keepass2.svg?branch=master)](https://travis-ci.org/azeemba/merge-keepass2)

Command line application to merge KeePass2 files into a new file.

## Usage

```
$ pip install -r requirements.txt
$ python merge.py  --help
Usage: merge.py [OPTIONS] [SRCFILES]... RESULTFILE

  Merge all keepass SRCFILES into a new file named RESULTFILE. Password for
  all files must be the same.

Options:
  --password TEXT  The password for keepass. You will be prompted if not
                   provided. Use `--password ""` if your database is only
                   protected by a keyfile. Environment variable
                   KEEPASS_PASSWORD can be set as well
  --keyfile TEXT   The path of a keyfile for keepass (optional). Environment
                   variable KEEPASS_KEYFILE can be set as well
  --help           Show this message and exit.
```

## Development

Test by running 

```
python -m pytest
```
