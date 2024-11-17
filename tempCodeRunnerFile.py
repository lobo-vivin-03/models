import json
from PyPDF2 import PdfReader
import re

pdf_file_path = r"E:/Projects/majorProject/syllabus.pdf"

def clean_text(text):
    """Clean text by removing unwanted characters and patterns."""
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespaces and newlines
    text = re.sub(r'\b\d+\s*Hours\b', '', text, flags=re.IGNORECASE)  # Remove patterns like "8 Hours"
    return text.strip()

def split_into_topics(text):
    """Split text into individual topics for array representation."""
    # Split the content into topics using common delimiters (e.g., periods, semicolons, commas)
    topics = re.split(r"[.;,]", text)
    return [topic.strip() for topic in topics if topic.strip()]

def extract_syllabus_content_as_array(pdf_filename):
    """Extract and structure syllabus content with module topics as an array."""
    try:
        with open(pdf_filename, 'rb') as f:
            pdf = PdfReader(f)
            syllabus_content = ""

            # Combine content from all pages
            for page in pdf.pages:
                page_content = page.extract_text()
                if page_content:
                    syllabus_content += page_content

            # Split by modules using regex
            module_pattern = r"(MODULE\s-\s[IV]+)"
            modules = re.split(module_pattern, syllabus_content)

            module_contents = {}
            course_outcomes = ""

            for i in range(1, len(modules), 2):
                module_title = modules[i].strip()  # Extract module title
                module_text = clean_text(modules[i + 1].strip())  # Clean module content

                # Separate "COURSE OUTCOMES" if it exists
                if "COURSE OUTCOMES" in module_text:
                    module_text, course_outcomes = re.split(r"COURSE OUTCOMES", module_text, maxsplit=1)
                    course_outcomes = clean_text(course_outcomes)

                # Split the cleaned text into topics
                topics = split_into_topics(module_text)
                module_contents[module_title] = topics

            return module_contents

    except FileNotFoundError:
        print(f"Error: The file '{pdf_filename}' was not found.")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

def main():
    print(f"Processing: {pdf_file_path}")

    # Extract syllabus content and store it in JSON
    modules_data = extract_syllabus_content_as_array(pdf_file_path)

    # Convert to JSON format
    json_data = json.dumps(modules_data, indent=4)
    print(json_data)

    # Save to a JSON file
    output_file_path = "syllabus_array.json"
    with open(output_file_path, "w", encoding="utf-8") as json_file:
        json_file.write(json_data)

    print(f"Data saved to {output_file_path}")

if __name__ == "__main__":
    main()
