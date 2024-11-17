
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

