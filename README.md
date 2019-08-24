# asprilo-mapfConverter

Provides a Python module for converting movingai's .map files to clingo compatible statements
as well as a small application to use it from the shell.

_Requires Python 3.6 or above_

## mapfconvert.py

A module containing functions and classes to convert a .map file to .lp.

## map2lp.py

An application for converting instance files using the **mapfconvert** module.

### Usage

From shell:

_$ python3 map2lp.py \[-h] [-i IN] [-o out] \[-nh] [-v {0,1,2} | -q]_

| **Short**^ | **Long**   | **Parameter type** | **Description**                         |
| :--------- | :--------- | :----------------- | :-------------------------------------- |
| -h         | --help     | None               | display help message and exit           |
| -i         | --input    | path (String)      | read from given file                    |
| -o         | --output   | path (String)      | write to file (create it, if necessary) |
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

### To-do list

* Exit program automatically without crashing if pipe is broken
* Add _compress_ option to reduce the size of output files
