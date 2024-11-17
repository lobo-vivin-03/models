
# Text Extraction Model

## Overview
This model processes PDF documents (syllabus files) to extract and structure syllabus content by splitting it into modules and topics. The extracted content is saved in a structured JSON format.

## Dependencies
To run this model, you will need the following Python packages:
- `PyPDF2`: A Python library to extract text from PDF files.
- `re`: Python's built-in module for regular expressions, used to clean and split text.
- `json`: Python's built-in module to handle JSON data.

## Installation Instructions
Before running the model, ensure that the required libraries are installed. You can install them using `pip`:

```bash
pip install PyPDF2
```
## Output
The model will process the input PDF file and save the extracted syllabus content in a JSON file located in the `models/text_extract` folder.

The output file is saved as `syllabus_array.json` in the following directory:

```bash
models/text_extract/syllabus_array.json
```
