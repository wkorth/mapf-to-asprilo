# Sollte über Stdin und Stdout funktionieren.
# Signatur:
# <name> [--input <path --output <path> --compress --verbose --help --sort]

import io


#terms = {".": ("node",), "T": ("tree", "node"), "W": ("water", "node")}


class TermConverter:
    """Converts specific characters to clingo literals."""

    def __init__(self, term_dict, template):
        self.terms = term_dict
        self.template = template
        self.termvalues = {term: [] for tup in self.terms.values()
                           for term in tup}

    def reset_values(self):
        for k in self.termvalues:
            self.termvalues[k].clear()

    def add_term(self, char, x, y):
        if char in self.terms:
            for term in self.terms[char]:
                self.termvalues[term].append((x, y))

    def term_counts(self):
        return [(key, len(self.termvalues[key])) for key in self.termvalues]

    def statements(self):
        """
        Returns a list of generators, each corresponding to one term.
        """
        # This works as a generator for generators, but behaves weirdly as a list of generators.
        # Why?
        return ((self.template.format(term, item[0], item[1][0], item[1][1])
                 for item in enumerate(sorted(self.termvalues[term]), 1))
                for term in self.termvalues)


def get_map_params(lines):
    return [tuple(line[:-1].rsplit(" ", 1)) for line in lines]


def generate_header(*args):
    """
    Takes an arbitrary amount of (String, int) tuple lists
    and generates a header for a logic file.
    """

    header = ('%' * 50) + "\n\n"
    for tuple_list in args:
        for pair in tuple_list:
            header += f"% {pair[0]}: {pair[1]}\n\n"
    header += ('%' * 50) + "\n\n"
    return header


def convert_file(source, target, term_dict, template, *, add_header=False):
    """
    Takes a file-like object and converts characters in the provided dictionary
    to clingo literals, one line at a time. Writes to specified target file.
    """
    # Abort if source file is empty
    if not source:
        return

    header_lines = 5    # TODO: write function to detect header
    orig_header = get_map_params([source.readline()
                                  for x in range(header_lines-2)])
    source.readline()

    converter = TermConverter(term_dict, template)

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
