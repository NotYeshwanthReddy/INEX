"""
Created on    : 15/04/2020
Developer    : NotYeshwanthReddy
Doc Type    : python
"""

"""
Templates are initially read from .yml files and then kept as objects of class.
"""

import os
import yaml
import pkg_resources
from collections import OrderedDict

from .template import Template



def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    """loads yml file as dictionary"""

    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)

    return yaml.load(stream, OrderedLoader)


def read_templates(folder=None):
    """
    Loads yaml files from template folder. Returns a list of Objects (instances of Template class).

    Args:
        path (:obj:`str`, optional, default=None):
            user defined folder where they stores their files, if None uses built-in templates
    Returns:
        templates (:obj: `InvoiceTemplate`):
            template which match based on keywords
    """

    templates = []

    if folder is None:
        folder = pkg_resources.resource_filename(__name__, "templates")

    for path, subdirs, files in os.walk(folder):
        for name in files:
            if name.endswith(".yml"):

                """Opening yml files"""
                # Check file encoding
                import chardet
                with open(os.path.join(path, name), "rb") as f:
                    encoding = chardet.detect(f.read())["encoding"]
                # Converting to dictionary using correct encoding
                import codecs
                with codecs.open(os.path.join(path, name), encoding=encoding) as template_file:
                    tpl = ordered_load(template_file.read())
                
                """Adding and Verifying fields in dictionary"""
                # Adding template name to dictionary
                tpl["template_name"] = name
                # Test if keywords field is in template
                assert "keywords" in tpl.keys(), "Missing keywords field."
                # Keywords as list, if only one.
                if type(tpl["keywords"]) is not list:
                    tpl["keywords"] = [tpl["keywords"]]

                # Converting dict to object
                tpl = Template(tpl)
                # appending to list
                templates.append(tpl)
    return templates
