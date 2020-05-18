"""
Created on    : 13/04/2020
Developer    : NotYeshwanthReddy
Doc Type    : python
"""

from input import pdftotext
from input import tesseract

from output import to_json

import argparse
import os
import logging

from extract.loader import read_templates


logger = logging.getLogger(__name__)


def create_parser():
    """Returns argument parser """

    parser = argparse.ArgumentParser(
        description="Extract structured data from PDF files and save to CSV or JSON."
    )

    parser.add_argument(
        "--output-date-format",
        dest="output_date_format",
        default="%Y-%m-%d",
        help="Choose output date format. Default: %%Y-%%m-%%d (ISO 8601 Date)",
    )

    parser.add_argument(
        "--output-name",
        "-o",
        dest="output_name",
        default="invoices-output",
        help="Custom name for output file. Extension is added based on chosen format.",
    )

    parser.add_argument(
        "--debug", dest="debug", action="store_true", help="Enable debug information."
    )

    parser.add_argument(
        "--template-folder",
        "-t",
        dest="template_folder",
        help="Folder containing invoice templates in yml file. Always adds built-in templates.",
    )

    parser.add_argument(
        "input_files",
        type=argparse.FileType("r"),
        nargs="+",
        help="File or directory to analyze.",
    )

    return parser


def select_input_module(name):
    if "pdf" in name.lower():
        return pdftotext
    if "png" in name.lower() or "tiff" in name.lower() or "jpg" in name.lower() or "jpeg" in name.lower():
        return tesseract


def extract_data(invoicefile, templates=None, input_module=pdftotext):
    """Extracts structured data from PDF/image invoices.

    This function uses the text extracted from a PDF file or image and
    pre-defined regex templates to find structured data.

    Args:
        invoicefile (`Str`):
            path of electronic invoice file in PDF,JPEG,PNG (example: "/home/duskybomb/pdf/invoice.pdf")
        templates (`list`, optional, default: `None`):
            Templates are loaded using `read_template` function in `loader.py`
        input_module (:obj:`{pdftotext, tesseract}`, optional, default:`pdftotext`):
            library to be used to extract text from given `invoicefile`,
    Returns:
        dict or False
            extracted and matched fields or False if no template matches
    """
    # Loading Templates if None
    if templates is None:
        templates = read_templates()
    # Extracting text
    extracted_str = input_module.to_text(invoicefile).decode("utf-8")
    # Logging extracted text
    logger.debug("START pdftotext result ===========================")
    logger.debug(extracted_str)
    logger.debug("END pdftotext result =============================")
    logger.debug("Testing {} template files".format(len(templates)))
    # iterate through all templates to find suitable template.
    for template in templates:
        # preprocess input
        optimized_str = template.prepare_input(extracted_str)
        # extract if keywords match
        if template.match_keywords(optimized_str):
            return template.extract_info(optimized_str)
    logger.error("No template for %s", invoicefile)
    return False


def main(args=None):
    """Take folder or single file and analyze each."""
    
    # Extract Args
    if args is None:
        parser = create_parser()
        args = parser.parse_args()
    
    # Configure Debug
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Load Templates
    templates = read_templates()
    
    # Load templates from external folder if set.
    if args.template_folder:
        templates += read_templates(os.path.abspath(args.template_folder))
    
    # Extracting data
    output = []
    for f in args.input_files:
        input_module = select_input_module(f.name)
        res = extract_data(f.name, templates=templates, input_module=input_module)
        res["file_name"] = f.name
        if res:
            logger.info(res)
            output.append(res)
        f.close()

    # Writing Output
    # TODO: fix output file
    to_json.write_to_file(output, args.output_name, args.output_date_format)


if __name__ == "__main__":
    main()
