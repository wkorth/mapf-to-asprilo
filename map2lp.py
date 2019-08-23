"""
Description of program here.
"""

import argparse
import sys

import mapfconvert


if __name__ == "__main__":

    terms = {".": ("node",), "T": ("tree", "node"), "W": ("water", "node")}

    statement_template = "init(object({},{}),value(at,({},{})).\n"


def get_args():
    parser = argparse.ArgumentParser(
        description="""
                    converts mapf instance files to clingo's 
                    input language (.map --> .lp)
                    """)
    parser.add_argument(
        "-i", "--input", metavar="IN", type=argparse.FileType("r"), default=sys.stdin, help="read from file")
    parser.add_argument(
        "-o", "--output", metavar="OUT", type=argparse.FileType("w"), default=sys.stdout, help="write to file")
    # parser.add_argument("-c", "--compress", type=int,
    #                     choices=[0, 1, 2], default=0, help="reduce number of statements in output")
    parser.add_argument("-nh", "--noheader",
                        help="omit the header of the output file", action="store_true")

    v_group = parser.add_mutually_exclusive_group()
    v_group.add_argument("-v", "--verbose", type=int,
                         choices=[0, 1, 2], default=1, help="set verbosity when writing to file")
    v_group.add_argument(
        "-q", "--quiet", action="store_true", help="set verbosity to 0")

    return parser.parse_args()


def main(terms, template):
    args = get_args()
    # Supress informational output if unwanted or interfering with result
    if args.quiet or args.input == sys.stdin:
        args.verbose = 0

    with args.input as source:
        with args.output as target:
            if args.verbose == 1:
                print(f"Converting {source.name}...")
            if args.verbose == 2:
                print(f"Converting {source.name} to {target.name}...")
            mapfconvert.convert_file(
                source, target, terms, template, add_header=not args.noheader)


if __name__ == "__main__":
    main(terms, statement_template)
