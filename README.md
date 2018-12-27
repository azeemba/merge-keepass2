merge-keepass2
==============

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
                   provided. Environment variable KEEPASS_PASSWORD can be set
                   as well
  --help           Show this message and exit.
```

## Development

Test by running 

```
python -m pytest
```