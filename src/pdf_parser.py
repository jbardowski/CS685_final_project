import os
import PyPDF2


def extract(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        num_pages = reader.numPages
        for page_num in range(num_pages):
            page = reader.getPage(page_num)
            text += page.extractText()  # adding to string... may be better to append str to list?
    return text


def save_text_to_file(text, filename):
    txt_filename = filename[:-4] + ".txt"  # Change extension to .txt
    with open(txt_filename, 'w') as file:
        file.write(text)


def main_extract(dir='./pdf_docs_raw'):
    # loop all pdf files in pdf_docs_raw, call extract function, then save to txt file in pdf_docs_parsed
    for filename in os.listdir(dir):
        if filename.endswith(".pdf"):
            print(f"About to parse {filename}...")
            f_path = os.path.join(dir, filename)
            text = extract(f_path)
            print("Parsed successfully, saving pdf_docs_parsed...")
            save_text_to_file(text, filename)


if __name__ == "__main__":
    main_extract()
