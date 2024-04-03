import os
import PyPDF2


def extract(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()  # adding to string... may be better to append str to list?
    return text


def main_extract(raw_dir='./raw_docs', parsed_dir='./parsed_docs'):
    # loop all files in pdf_docs_raw, call extract function if not already parsed, then save to txt file in parsed_dir.
    already_parsed = os.listdir(parsed_dir)

    for filename in os.listdir(raw_dir):
        if filename.endswith(".pdf"):
            if filename.replace(".pdf", ".txt") in already_parsed:
                print(f"{filename} already parsed, skipping.")
                break
            print(f"About to parse {filename}...")
            f_path = os.path.join(raw_dir, filename)
            text = extract(f_path)

            print(f" Success, saving to txt...")
            s_path = os.path.join(parsed_dir, filename.replace('pdf', 'txt'))
            with open(s_path, 'w') as file:
                file.write(text)


if __name__ == "__main__":
    main_extract()
