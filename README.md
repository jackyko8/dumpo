# Dumpo Python Object Serialiser

Dumpo serialises a Python object recursively to arbitrary levels, optionally in a JSON like format.

Synopsis:
```
from dumpo import *
obj_str = dumpo(obj)
```

Keyword arguments:

| Argument          | Description                                                  | Type            | Default Value |
| ----------------- | ------------------------------------------------------------ | --------------- | ------------- |
| as_is             | List of data type names to be shown as is. i.e., `print(f'{obj}')` | List or string | `[]`          |
| as_is_tag         | String to append to a data item serialised "as is"           | String          | `"<as_is>"` |
| compressed        | If True compress list to a single line instead of one data item per line | Boolean         | `True`        |
| debug             | If True append debug information to each data item           | Boolean         | `False`       |
| excluded          | List of item names to be excluded from serialisation         | List or string  | `[]`          |
| excluded_tag      | String to replace excluded data items. Blank to hide all excluded data items. | String        | `"<excluded>"` |
| expand_keys       | If True serialise structured item keys, else show them as a string. i.e., `print(f'{itemKey}')` | Boolean         | `False`       |
| include_functions | If True include object functions (function names only with no code) | Boolean         | `False`       |
| indent            | String used for indentation, repeat for the number of levels | String          | `"\| "`   |
| item_quotes       | Quotation marks for item keys - a 2-character string for open and close respectively; a 1-character string if open and close are the same; blank means no quotation marks for item keys | String          | `None`        |
| json_like         | If True serialise in JSON format - implying `indent="  "` and `item_quotes = '"'`, and `False` for `show_types` and `show_all_types`. | Boolean         | `False`       |
| maxdepth          | Maximum levels to serialise                                  | Integer         | `5`           |
| quotes            | Quotation marks for data items - a 2-character string for open and close respectively; a 1-character string if open and close are the same; blank means no quotation marks for data items | String          | `""`  |
| show_all_types    | If True prepend the data type to each data item of all types, e.g., `<type>{ ... }`    | Boolean       | `True`        |
| show_types        | If True prepend the data type to each data item except for simple types, e.g., `<type>{ ... }` | Boolean        | `True`        |
| too_deep_tag      | String to replace data items or structures below the `maxdepth`th level | String         | `"<too_deep>"` |

[Dumpo at GitHub](https://github.com/jackyko8/dumpo)
