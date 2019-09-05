"""
A module containing functions and classes to convert a mapf instance
from movingai's .map format file to clingo's .lp format.
"""

import logging


class TermConverter:
    """
    Converts specific characters to clingo literals.
    Tracks amount of statements translated and may return
    all statements in a nested generator.
    """

    def __init__(self, term_dict, ignore, template):
        """
        Initializes a TermConverter with the given attributes.
        """

        self.terms = term_dict
        self.ignore = ignore
        self.template = template
        self.termvalues = {term: [] for tup in self.terms.values()
                           for term in tup}

    def reset_values(self):
        """
        Resets the tracked usages of terms to zero.
        """

        for k in self.termvalues:
            self.termvalues[k].clear()

    def add_term(self, char, x, y):
        """
        Adds all terms corresponding to the character to termvalues,
        as well as their coordinates.
        """

        if char in self.terms:
            for term in self.terms[char]:
                self.termvalues[term].append((x, y))
        elif char is not "\n" and char not in self.ignore:
            logging.warning(
                f"Found unhandled character '{char}' at ({x},{y})!")

    def term_counts(self):
        """
        Returns a tuple list containing all terms and their amount of uses.
        """

        return [(key, len(self.termvalues[key])) for key in self.termvalues]

    def statements(self):
        """
        Returns a list of generators, each corresponding to one term.
        """

        # This works as a generator for generators,
        # but behaves weirdly as a list of generators.
        # Why?
        return ((self.template.format(term, item[0], item[1][0], item[1][1])
                 for item in enumerate(sorted(self.termvalues[term]), 1))
                for term in self.termvalues)


def read_map_params(map_file):
    """
    Reads the header of a .map file (until the "map" line) and returns the
    map parameters as tuples in a list.
    """

    params = []
    for line in map_file:
        if line.strip() == "map":
            break
        params.append(tuple(line[:-1].rsplit(" ", 1)))
    return params


def generate_header(*args):
    """
    Takes an arbitrary amount of tuple lists
    and generates a header for a logic file.
    """

    header = ('%' * 50) + "\n\n"
    for tuple_list in args:
        for pair in tuple_list:
            header += f"% {pair[0]}: {pair[1]}\n\n"
    header += ('%' * 50) + "\n\n"
    return header


def convert_file(source, target, term_dict, ignore, template, *, add_header=False):
    """
    Takes a file-like object and converts characters in the provided dictionary
    to clingo literals following a template, one line at a time.
    Writes to specified target file.

    Arguments:
    source - file-like object to read from
    target - file like object to write to
    term_dict - dictionary containing characters and their translations
    template - String showing the scheme of translated statements
    add_header - whether to prepend a header to the output
    """

    orig_header = read_map_params(source)
    converter = TermConverter(term_dict, ignore, template)

    y_coord = 0
    for line in source:
        y_coord += 1
        for x_coord, char in enumerate(line, 1):
            converter.add_term(char, x_coord, y_coord)

    if add_header:
        target.write(generate_header(orig_header, converter.term_counts()))

    for generator in converter.statements():
        for statement in generator:
            target.write(statement)
