"""
Created on    : 17/04/2020
Developer    : NotYeshwanthReddy
Doc Type    : python
"""

import subprocess
from distutils import spawn


def to_text(path):
    """Wraps Tesseract OCR.
    Args:
        path (str):
            path of electronic invoice in JPG or PNG format
    Returns:
        output (str):
            returns extracted text from image in JPG or PNG format
    Raises:
        EnvironmentError:
            requirements not installed
    """

    # Check for dependencies. Needs Tesseract and Imagemagic.
    if not spawn.find_executable("tesseract"):
        raise EnvironmentError("tesseract not installed.")
    if not spawn.find_executable("convert"):
        raise EnvironmentError("imagemagick not installed.")

    # convert = "convert -density 350 %s -depth 8 tiff:-" % (path)
    convert = [
        "convert",
        "-density",
        "350",
        path,
        "-depth",
        "8",
        "-alpha",
        "off",
        "png:-",
    ]
    # converting image to png format
    p1 = subprocess.Popen(convert, stdout=subprocess.PIPE)
    # extracting text with tesseract OCR.
    tess = ["tesseract", "stdin", "stdout"]
    p2 = subprocess.Popen(tess, stdin=p1.stdout, stdout=subprocess.PIPE)

    out, err = p2.communicate()

    return out
