import io
import time
from pdfminer.high_level import extract_text

def parse_esg_report(filepath):
    """
    Parses an ESG report in PDF format, tracks parsing time, and returns the extracted text.

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

# Example usage
esg_report_path = "src/raw_docs/DE_sustain_report.pdf" 
extracted_text, parse_time = parse_esg_report(esg_report_path)

print(extracted_text)

print(f"Document parsed in {parse_time:.4f} seconds")



# Save parsed text
with open("src/parsed_docs/DE_sustain_report_parsed.txt", 'w', encoding="utf-8") as output_file:
    output_file.write(extracted_text) 