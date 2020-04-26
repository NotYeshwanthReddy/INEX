"""
Created on    : 14/04/2020
Developer    : NotYeshwanthReddy
Doc Type    : python
"""

import json
import datetime


def myconverter(o):
    """function to serialise datetime"""
    if isinstance(o, datetime.datetime):
        return o.__str__()


def write_to_file(data, path, date_format="%Y-%m-%d"):
    """Export extracted fields to json
    Appends .json to path if missing and generates json file in specified directory, if not then in root

    Args:
        data (:obj:`Dict[field: value]`):
            Dictionary of extracted fields
        path (:obj:`str`):
            directory to save generated json file
        date_format (:obj:`str`, optional, defaults to "%Y-%m-%d"):
            Date format used in generated file
    """
    if path.endswith(".json"):
        filename = path
    else:
        filename = path + ".json"

    with open(filename, "w", encoding="utf-8") as json_file:
        for line in data:
            for k, v in line.items():
                if k.startswith("date") or k.endswith("date"):
                    line[k] = v.strftime(date_format)
        # print(type(json))
        # print(json)
        json.dump(
            data,
            json_file,
            indent=4,
            sort_keys=True,
            default=myconverter,
            ensure_ascii=False,
        )
