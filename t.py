#!/usr/bin/env python

"""A script that helps generate router configuration from templates.
"""

import os
import sys
import argparse
import csv
import jinja2
from jinja2 import meta


def get_template_var_list(config_template):

    j2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='.'))
    j2_template_source = j2_env.loader.get_source(j2_env, config_template)[0]
    j2_parsed_content = j2_env.parse(j2_template_source)
    return(meta.find_undeclared_variables(j2_parsed_content))


def generate_csv_header(config_template):
    template_vars = sorted(list(get_template_var_list(config_template)))
    pre, _ = os.path.splitext(config_template)

    with open(pre + ".csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(template_vars)
        print("Header variables saved to " + pre + ".csv")


def generate_config(config_template, config_data, config_outdir):

    # init jinja2 environment
    j2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='.'))
    j2_template = j2_env.get_template(config_template)

    # read csv data
    totalrows = 0
    with open(config_data) as csv_file:
        # initialize reader object and protect against non-uniform csv files
        # missing values will be empty strings
        csv_reader = csv.DictReader(csv_file, restval="WARNING_VALUE_MISSING")

        # check if all the template vars are found in the csv
        if not all(x in csv_reader.fieldnames for x in get_template_var_list(config_template)):
            sys.exit('Not all variables in {} are found in {}'.format(config_template, config_data))

        # create config output dir
        out_directory = os.path.join(os.path.dirname(config_template), config_outdir)
        if not os.path.exists(out_directory):
            os.makedirs(out_directory)

        for row in csv_reader:
            # render template for each row from the csv file and write it to disk
            j2_rendered_template = j2_template.render(row)
            out_filename = os.path.join(out_directory, "cfg-" + str(csv_reader.line_num-1))

            with open(out_filename, mode="w") as out_file:
                out_file.write(j2_rendered_template)
                totalrows += 1

    print("Generated {} files in {}/".format(totalrows, out_directory))

def main(arguments):

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('operation', help="gencfg, csvheader")
    parser.add_argument('-t', '--template', help="config template file (jinja2)")
    parser.add_argument('-d', '--data', help="config data file (csv)")
    parser.add_argument('-o', '--outdir', help="output directory (default=configs)", default="configs")

    args = parser.parse_args(arguments)

    if args.operation == "gencfg":
        if args.template and args.data:
            generate_config(args.template, args.data, args.outdir)
        else:
            sys.exit("Template (-t) and data (-d) files must be specified.")
    elif args.operation == "csvheader":
        if args.template:
            generate_csv_header(args.template)
        else:
            sys.exit("Template (-t) file must be specified.")
    else:
        sys.exit("Invalid operation. Use gencfg to apply data to a template or " +
                 "csvheader to extract variables from a template.")

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
