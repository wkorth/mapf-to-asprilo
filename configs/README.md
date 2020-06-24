# Config files

These YAML-files determine how the instance/scenario is translated.
They need to contain the following parameters:

## Parameters for mapf-instances

- *term_dict*: Contains symbols and their translation.

- *ignore_list*: Contains symbols that should not be translated.

- *statement_template*: Contains a logic statement as a string, with four *{}* as placeholder for name, index and coordinates of the object.

## Parameters for mapf-scenarios

- *param_dict*: Contains parameters and statement templates for their values.