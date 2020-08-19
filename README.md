# mapf-to-asprilo

Provides a Python module for converting [movingai's .map files](https://www.movingai.com/benchmarks/index.html "www.movingai.com/benchmarks") to clingo compatible statements
as well as a small application to use it from the shell.

**Note that the upper left corner of the map will have the coordinates (1,1) in converted files, in contrast to the .map files, where it is usually (0,0).**

_Requires Python 3.6 or above_

## mapfconvert.py

A module containing functions and classes to convert a .map or .scen file to .lp.

## map-to-lp.py

An application for converting instance files using the **mapfconvert** module.

### Usage

From shell:

map_to_lp \[-h] [-i IN] [-o out] \[-nh] [-v {0,1,2} | -q]_

| **Short**  | **Long**   | **Parameter type** | **Description**                         |
| :--------- | :--------- | :----------------- | :-------------------------------------- |
| -h         | --help     | None               | display help message and exit           |
| -i         | --input    | path (String)      | read from given file                    |
| -o         | --output   | path (String)      | write to file (create it, if necessary) |
| -c         | --config   | path (String)      | use YAML config file                    |
| -nh        | --noheader | boolean            | omit the header of the output           |
| -v         | --verbose  | int {0,1,2}        | set verbosity (when writing to file)    |
| -q         | --quiet    | None               | set verbosity to 0                      |

#### I/O

By default, map2lp reads from stdin and prints to stdout.
Both input and output can be changed by giving a path to a file using the respective options.

#### Header

The program prepends a clingo comment containing some statistics about the instance to its output.
This can be supressed by using the _noheader_-option.

#### Verbosity

When map2lp starts working on a file, it will print a small message to stdout.
Depending on its verbosity value, that message contains:

* verbose 0: Nothing, message is omitted
* verbose 1: The name of the input file
* verbose 2: The names of both input and output file

Verbosity is always 0 when printing the output to stdout or when using the _quiet_-option.

## scen-to-lp.py

An application for converting scenario files using the **mapfconvert** module.

### Usage

Equivalent to the usage of **map-to-lp**.

## To-do list

* Exit program automatically without crashing if pipe is broken
