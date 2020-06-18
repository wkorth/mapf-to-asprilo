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
        Returns a generator of generators, each corresponding to one term.
        """

        return ((self.template.format(term, item[0], item[1][0], item[1][1])
                 for item in enumerate(sorted(self.termvalues[term]), 1))
                for term in self.termvalues)


class ScenarioConverter:

    def __init__(self, param_dict):
        """
        Initializes a ScenarioConverter with the given dictionary.
        """

        self.param_dict = param_dict
        self.parameter_amount = len(self.param_dict)
        self.param_values = {param: [] for param in self.param_dict}
        self.scenario_amount = 0

    def reset_values(self):
        """
        Deletes all saved parameter values.
        """

        for key in self.param_values:
            self.param_values[key].clear()
        self.scenario_amount = 0

    def add_scenario(self, line):
        """
        Reads a line containing a scenario and adds read parameters to the dictionary.
        """

        line = line.split()
        if len(line) != self.parameter_amount:
            logging.warning(
                f"""Omitting scenario with {len(line)} parameters 
                            (expected {self.parameter_amount})!""")
        else:
            # Does not explicitly enforce correct order of keys
            for key in self.param_values:
                self.param_values[key].append(line.pop(0))
            self.scenario_amount += 1

    def statements(self, *, maximum=0):
        """
        Returns a list of generators, each corresponding to one parameter,
        up to the requested amount of scenarios.
        """

        # Set maximum to list length if invalid or standard value
        if maximum < 1 or maximum > self.scenario_amount:
            maximum = self.scenario_amount

        return ((self.param_dict[param].format(self.param_values[param][i], index=i+1)
                 for i in range(maximum) if self.param_dict[param] is not None)
                 for param in self.param_values)


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


def read_scen_params(scen_file):
    """
    Reads the header of a .scen file (until and including the "version" line) and returns the
    parameters as tuples in a list.
    """

    params = []
    for line in scen_file:
        params.append(tuple(line[:-1].rsplit(" ", 1)))
        if params[-1][0].lower() == "version":
            break
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


def convert_map(source, target, term_dict, ignore, template, *, add_header=False):
    """
    Takes a file-like object and converts characters in the provided dictionary
    to clingo literals following a template.
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


def convert_scen(source, target, param_dict, *, add_header=False):
    """
    Takes a file-like object following movingai's .scen-format and converts
    characters to clingo literals following the provided dictionary.
    Writes to specified target file.

    Arguments:
    source - file-like object to read from
    target - file like object to write to
    param_dict - dictionary of dictionaries (<parameter>: <template>)
    add_header - whether to prepend a header to the output
    """

    orig_header = read_scen_params(source)
    converter = ScenarioConverter(param_dict)

    for line in source:
        converter.add_scenario(line)

    if add_header:
        target.write(generate_header(orig_header))

    for generator in converter.statements():
        for statement in generator:
            target.write(statement)
