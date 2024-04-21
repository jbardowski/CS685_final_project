# import pdfplumber
# import re
# import time
# import os

# def extract_sentences(pdf_path, output_file):
#     sentences = []
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text = page.extract_text()
#             # Split the text into lines
#             lines = text.split('\n')
#             for line in lines:
#                 # Remove empty lines
#                 if line.strip():
#                     # Split the line into sentences
#                     line_sentences = re.split(r'[.!?]\s*', line)
#                     sentences.extend(line_sentences)

#     # Save sentences to the output file
#     with open(output_file, 'w', encoding='utf-8') as file:
#         for sentence in sentences:
#             file.write(sentence.strip() + '\n')

# # Example usage
# start_time = time.time()
# script_dir = os.path.dirname(os.path.abspath(__file__))
# pdf_path = os.path.join(script_dir, 'raw_docs', 'DE_sustain_report.pdf')
# output_file = os.path.join(script_dir, 'extracted_sentences.txt')
# extract_sentences(pdf_path, output_file)


# end_time = time.time()
# parse_time = end_time - start_time

# print(f"Document parsed in {parse_time:.4f} seconds")


import re
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
import os

def extract_sentences(page_layout):
    sentences = []
    for element in page_layout:
        if isinstance(element, LTTextBox):
            for text_line in element:
                if isinstance(text_line, LTTextLine):
                    line_text = text_line.get_text()
                    if line_text.strip():
                        line_sentences = re.split(r'[.!?]\s*', line_text)
                        sentences.extend(line_sentences)
    return sentences

def extract_sentences_from_pdf(pdf_path):
    all_sentences = []
    with open(pdf_path, 'rb') as pdf_file:
        laparams = LAParams()
        pages = extract_pages(pdf_file, laparams=laparams)
        for page_layout in pages:
            page_sentences = extract_sentences(page_layout)
            all_sentences.extend(page_sentences)
    return all_sentences

# Example usage
script_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(script_dir, 'raw_docs', 'DE_sustain_report.pdf')
output_file = os.path.join(script_dir, 'extracted_sentences.txt')
sentences = extract_sentences_from_pdf(pdf_path)

# Save sentences to the output file
with open(output_file, 'w', encoding='utf-8') as file:
    for sentence in sentences:
        file.write(sentence.strip() + '\n')
