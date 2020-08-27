#!/usr/bin/env python

"""
An application for converting scenario files from movingai's .scen format file
to clingo's .lp format. Uses stdin and stdout by default.
"""

import argparse
import logging
import sys
import yaml
import pathlib

from . import mapfconvert


def get_config(cfg):
    """
    Attempts to read parameters from a YAML file and uses defaults when given None.
    """

    if cfg is None:
        param_dict = {
            "bucket": None,
            "map": 'map("{}",{}).\n',
            "map_width": "map_width({},{}).\n",
            "map_height": "map_height({},{}).\n",
            "start_x": "start_x({},{}).\n",
            "start_y": "start_y({},{}).\n",
            "goal_x": "goal_x({},{}).\n",
            "goal_y": "goal_y({},{}).\n",
            "optimal_length": None
        }

    else:
        with cfg as stream:
            try:
                cfg_dict = yaml.safe_load(stream)
            except yaml.YAMLError as exception:
                logging.error(exception)
                sys.exit("Error while parsing config file")

            param_dict = cfg_dict["param_dict"]

    return param_dict


def get_args():
    """
    Defines and parses command line arguments.
    """

    parser = argparse.ArgumentParser(
        description="""
                    converts mapf scenario files to clingo's
                    input language (.scen --> .lp)
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


def main():
    """
    Converts specified files from .scen to .lp.

    Arguments:
    args - an argparse.Namespace object
    param_dict - dictionary containing scenario parameters and their statements
    """

    # Get arguments
    args = get_args()

    # Supress informational output if unwanted or interfering with result
    if args.quiet or args.output == sys.stdout:
        args.verbose = 0

    param_dict = get_config(args.config)

    with args.input as source:
        with args.output as target:
            if args.verbose == 1:
                print(f"Converting {source.name}...")
            if args.verbose == 2:
                print(f"Converting {source.name} to {target.name}...")
            mapfconvert.convert_scen(
                source, target, param_dict,
                add_header=not args.noheader)


if __name__ == "__main__":
    sys.exit(main())
