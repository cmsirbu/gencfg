# gencfg

A Python3 script that applies csv data to configuration templates (in jinja2 format).

## Requirements

- [Python](https://www.python.org/) **3.x**
- [Jinja2](http://jinja.pocoo.org/)

To install dependencies, run `pip3 install -r requirements.txt` after cloning the repo.

## Usage

Script has two modes:

1. Generate a `csv` header from a template file: `t.py csvheader -t template.j2`
2. Generate device configuration based on a template and data: `t.py gencfg -t template.j2 -d data.csv`

The `csv` file MUST have a header row defining the variables used in the template and all of the variables must be present. Any extra columns will be ignored.

## Example

