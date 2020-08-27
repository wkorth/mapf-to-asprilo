---
title: mapf-to-asprilo
layout: page
output:
    html_document:
        toc: true
        toc_depth: 3
        toc_float: true
---

## About

Provides a Python module for converting [movingai's .map files](https://www.movingai.com/benchmarks/index.html "www.movingai.com/benchmarks") to clingo compatible statements
as well as a small application to use it from the shell.

**Note that the upper left corner of the map will have the coordinates (1,1) in converted files, in contrast to the .map files, where it is usually (0,0).**

_Requires Python 3.6 or above_

## Installation

The preferred method of inbstalling the converter is by using [conda](https://conda.io/).

```bash
conda install -c wkorth mapf-to-asprilo
```

Manual Installation from the [Github-repository](https://github.com/wkorth/mapf-to-asprilo) is possible, but neither encouraged nor further supported.

## Requirements

The converter requires the following software to function:

1. [clingo5](http://github.com/potassco/clingo)>=5.3.0
2. [Python interpreter version >=3.6.x](http://www.python.org)

## Usage

The module comes with two scripts:

1. **map-to-lp** converts instance files (typically ending with _.map_)
2. **scen-to-lp** converts scenario files (typically ending with _.scen_)


### Shell commands

Both scripts are invoked over the command line and offer the same command options.

From shell:

```bash
map_to_lp \[-h] [-i IN] [-o out] \[-nh] [-v {0,1,2} | -q]_
```

or

``` bash
map_to_lp \[-h] [-i IN] [-o out] \[-nh] [-v {0,1,2} | -q]_
```

### Command options

| **Short**  | **Long**   | **Parameter type** | **Description**                         |
| :--------- | :--------- | :----------------- | :-------------------------------------- |
| -h         | --help     | None               | display help message and exit           |
| -i         | --input    | path (String)      | read from given file                    |
| -o         | --output   | path (String)      | write to file (create it, if necessary) |
| -c         | --config   | path (String)      | use YAML config file                    |
| -nh        | --noheader | boolean            | omit the header of the output file      |
| -v         | --verbose  | int {0,1,2}        | set verbosity (when writing to file)    |
| -q         | --quiet    | None               | set verbosity to 0                      |

#### I/O

By default, map2lp reads from _stdin_ and prints to _stdout_.
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

### Configuration files

The translation behaviour of both scripts can (and should) be customized using YAML-files.
These configuration files specify how the objects of the instances and parameters of the scenarios are to be named in ASP.

Three config files are given as examples for expected usecases in the _configs_-directory:

1. **movingai.yml** is for instances like those on [movingai.com](https://www.movingai.com/benchmarks/index.html).
2. **simple.yml** only translates the traversible area of the instance, losing all other objects.
3. **vizmark.yaml** translates objects as ASPRILO-objects depictable with the [asprilo-visualizer](https://github.com/potassco/asprilo/tree/master/visualizer).

### Configuration parameters

The configuration files contain important parameters which can be changed to customize behaviour.

Three of them are used by **map-to-lp** when translating instances:

* term_dict
* ignore_list
* statement_template

One is used by **scen-to-lp** when translating scenarios:

* param_dict

As long as the config file given to a script contains its respective parameter(s), the scripts will work.

#### term_dict

A dictionary/map containing characters used in the instance file as _keys_ and lists with names(strings) as _values_.
Every occurence of a symbol in the instance will be translated to ASP as one object with the given name for each element of the list.

Example:

```yaml
"term_dict":
    "G":
        - "node"
    "T":
        - "node"
        - "tree"
```

The above dictionary would translate each "G" in the instance as one _node_-ASPRILO-object.
Every "T" in the Instance would be translated as **both** a _node_ and a separate _tree_ (on the same coordinates).

#### ignore_list

A list containing characters which are to be skipped when translating the instance. All characters in the instance file must be mentioned in either _term\_dict_ or _ignore\_list_, or it will not be handled and the translation will stop and throw an error message.

#### statement_template

A String showing how the finished ASP-atom should look after translation, leaving braces for (in that order) _name_, _index_ and _coordinates_.

Example:

```yaml
"statement_template": "init(object({},{}),value(at,({},{}))).\n"
```

This is the template for object notation the way it is done in ASPRILO.

#### param_dict

A dictionary/map containing scenario parameters as _keys_ and ASP statement templates (strings) as _values_.

All parameters in the scenario file must be handled, but the value may be set to _~_, in which case the parameter will be ignored.
The templates are written similar to **map-to-lp**'s _statement\_template_.

Example:

```yaml
"param_dict":

"bucket": ~

"map": "map(\"{}\",{}).\n"

"map_width": "map_width({},{}).\n"

"map_height": "map_height({},{}).\n"

"start_x": "start_x({},{}).\n"

"start_y": "start_y({},{}).\n"

"goal_x": "goal_x({},{}).\n"

"goal_y": "goal_y({},{}).\n"

"optimal_length": ~
```

## Note

This program is still in an early and unpolished, albeit functional, state. If you find errors, bugs or have questions, please raise the issue on [Github](https://github.com/wkorth/mapf-to-asprilo).