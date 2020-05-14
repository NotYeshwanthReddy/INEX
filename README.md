# INEX
Extracting Invoice Data from various file formats.

## Problem Statement:
Extracting structured data from invoices which are in various formats (PDF, Word, e-invoice) and saving them to an excel sheet.

## Explanation: 
The invoices provided will be in multiple formats and languages. Some are PDFs, some are word documents while others are e-invoices. None of them follow a fixed template. Few are scanned copies of original invoice also, which need OCR to extract data.

The task is to extract data from these invoices using OCR and structuring it uisng Deeplearning. The purpose of digitilizing these invoices and saving them in one place is to 
* Reduced maintainence costs
* Improve account reconciliation
* Enhance compliance
* Prevent errors, losses and frauds

## Usage:
Run as-
<pre>    python inex.py [path_to_file|folder] </pre>

Example-
<pre>    python inex.py example/ </pre>
