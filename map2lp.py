"""
An application for converting instance files from movingai's .map format file
to clingo's .lp format. Uses stdin and stdout by default.
"""

import argparse
import sys

import mapfconvert


if __name__ == "__main__":

    term_dict = {".": ("node",), "T": ("tree", "node"), "W": ("water", "node")}

    statement_template = "init(object({},{}),value(at,({},{})).\n"


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

    # TODO: parser.add_argument("-c", "--compress", type=int,
    #                     choices=[0, 1, 2], default=0,
    #                     help="reduce number of statements in output")

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


def main(args, term_dict, template):
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

    with args.input as source:
        with args.output as target:
            if args.verbose == 1:
                print(f"Converting {source.name}...")
            if args.verbose == 2:
                print(f"Converting {source.name} to {target.name}...")
            mapfconvert.convert_file(
                source, target, term_dict, template,
                add_header=not args.noheader)


if __name__ == "__main__":
    main(get_args(), term_dict, statement_template)
