import io
import time
import os
from pdfminer.high_level import extract_text

def parse_esg_report(filepath):
    """ Parses an ESG report in PDF format, tracks parsing time, and returns the extracted text.
    Args:
        filepath (str): Path to the ESG report PDF file.
    Returns:
        tuple: (str, float) The extracted text from the PDF report and the time taken (in seconds).
    """
    start_time = time.time()
    with open(filepath, 'rb') as f:
        raw_text = extract_text(f)
    end_time = time.time()
    parse_time = end_time - start_time
    return raw_text, parse_time

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the raw documents folder
raw_docs_path = os.path.join(script_dir, "raw_docs")

# Path to the parsed documents folder
parsed_docs_path = os.path.join(script_dir, "parsed_docs")

# Create the parsed documents folder if it doesn't exist
os.makedirs(parsed_docs_path, exist_ok=True)

# Get a list of PDF files in the raw documents folder
pdf_files = [f for f in os.listdir(raw_docs_path) if f.endswith(".pdf")]

for pdf_file in pdf_files:
    # Print log statement for the current file
    print(f"Processing file: {pdf_file}")

    # Parse the PDF file
    esg_report_path = os.path.join(raw_docs_path, pdf_file)
    extracted_text, parse_time = parse_esg_report(esg_report_path)

    # Print log statement for the parsing time
    print(f"Document parsed in {parse_time:.4f} seconds")

    # Save the parsed text to a file
    output_filename = os.path.splitext(pdf_file)[0] + "_parsed.txt"
    output_filepath = os.path.join(parsed_docs_path, output_filename)
    with open(output_filepath, 'w', encoding="utf-8") as output_file:
        output_file.write(extracted_text)

    # Print log statement for successful parsing and saving
    print(f"Parsed text saved to: {output_filepath}\n")