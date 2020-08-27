#!/usr/bin/env python

"""
An application for converting instance files from movingai's .map format file
to clingo's .lp format. Uses stdin and stdout by default.
"""

import argparse
import logging
import sys
import yaml
import pathlib
import mapfconvert


def get_config(cfg):
    """
    Attempts to read parameters from a YAML file and uses defaults when given None.
    """
    
    if cfg is None:
        # dictionary containing characters as keys and their translations as values
        term_dict = {".": ["node"], "G": ["node"], "T": ["tree", "node"],
                 "S": ["swamp", "node"], "W": ["water", "node"]}
        
        # list of characters to ignore
        ignore_list = ["@", "O"]

        # empty template for translated statements
        statement_template = "init(object({},{}),value(at,({},{}))).\n"

    else:
        with cfg as stream:
            try:
                cfg_dict = yaml.safe_load(stream)
            except yaml.YAMLError as exception:
                logging.error(exception)
                sys.exit("Error while parsing config file")

        term_dict = cfg_dict["term_dict"]
        ignore_list = cfg_dict["ignore_list"]
        statement_template = cfg_dict["statement_template"]

    return term_dict, ignore_list, statement_template


def get_args():
    """
    Defines and parses command line arguments.
    """

    parser = argparse.ArgumentParser(
        description="""
                    converts mapf instance files to clingo's
                    input language (.map --> .lp)
                    """)

    parser.add_argument(
        "-i", "--input", metavar="IN", type=argparse.FileType("r"),
        default=sys.stdin, help="read from file")

    parser.add_argument(
        "-o", "--output", metavar="OUT", type=argparse.FileType("w"),
        default=sys.stdout, help="write to file")

    parser.add_argument("-c", "--config", metavar="CFG",
                        type=argparse.FileType("r"), help="use YAML configuration file")

    parser.add_argument("-nh", "--noheader",
                        help="omit the header of the output file",
                        action="store_true")

    v_group = parser.add_mutually_exclusive_group()

    v_group.add_argument("-v", "--verbose", type=int,
                         choices=[0, 1, 2], default=1,
                         help="set verbosity when writing to file")

    v_group.add_argument(
        "-q", "--quiet", action="store_true", help="set verbosity to 0")

    return parser.parse_args()


def main(args):
    """
    Converts specified files from .map to .lp.

    Arguments:
    args - an argparse.Namespace object
    term_dict - dictionary containing characters and their translations
    template - String showing the scheme of translated statements
    """

    # Supress informational output if unwanted or interfering with result
    if args.quiet or args.output == sys.stdout:
        args.verbose = 0

    term_dict, ignore, template = get_config(args.config)

    with args.input as source:
        with args.output as target:
            if args.verbose == 1:
                print(f"Converting {source.name}...")
            if args.verbose == 2:
                print(f"Converting {source.name} to {target.name}...")
            mapfconvert.convert_map(
                source, target, term_dict, ignore, template,
                add_header=not args.noheader)


if __name__ == "__main__":
    main(get_args())
