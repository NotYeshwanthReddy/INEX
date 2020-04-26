"""
Created on    : 13/04/2020
Developer    : NotYeshwanthReddy
Doc Type    : python
"""

import subprocess
from distutils import spawn


def to_text(path):
    """Using pdftotext
    Args:
        path (str): 
            path of electronic invoice in PDF
    Returns:
        output (str):
            returns extracted text from pdf
    Raises:
        EnvironmentError:
            If pdftotext library is not found
    """
    if spawn.find_executable("pdftotext"):
        # print("found pdftotext")
        out, err = subprocess.Popen(
            ["pdftotext", "-layout", "-enc", "UTF-8", path, "-"], stdout=subprocess.PIPE
        ).communicate()
        return out
    else:
        raise EnvironmentError(
            "pdftotext not installed."
        )
