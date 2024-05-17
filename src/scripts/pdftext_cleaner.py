import re, nltk.data, os, time
from pdfminer.high_level import extract_text
# from transformers import T5Tokenizer, TFT5ForConditionalGeneration
"""
Take a list of lines from a file and return a list of "well formed" sentences. A well formed sentence
is defined by a capitalized first word, and a '.' at the end. This parser works by buffering multiple lines
together until a line break. Then it tries to extract each sentece from the buffer. If partial sentences are found
(usually all or only the last) it adds them to an overflow for later consideration. See parse_overflow

lines: list of each line in the file
parse_overflow: flag to enable checking a cache of broken lines that don't quite form a sentence 
                and are separated by a "\n" token. When combined this might result in a sentence.
                Useful for files where formatting is awkard and each string has a \n in between. 
                Check the formatting of the input file before using this flag
                e.g:
                this is a complete
                
                sentence but it is
                
                separated by newlines
                
                ==>
                this is a complete sentence but it is separated by newlines
debug: various debugging info to see what the parser is trying to do. 
                
"""

def re_punctuate(text):
    pass
    # tokenizer = T5Tokenizer.from_pretrained('SJ-Ray/Re-Punctuate')
    # model = TFT5ForConditionalGeneration.from_pretrained('SJ-Ray/Re-Punctuate')

    # inputs = tokenizer.encode("punctuate: " + text, return_tensors="tf") 
    # result = model.generate(inputs)

    # decoded_output = tokenizer.decode(result[0], skip_special_tokens=True)
    # return decoded_output

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

def pdftext2sents(lines, parse_overflow=False, debug=False):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    final_data = []
    buffer = ""
    buffer_overflow = ""
    add_period = False
    print("Raw Line Count: ", len(lines))
    for i, l in enumerate(lines):            
        if l == "\n":
            if i+1 < len(lines) and ("." not in lines[i+1].strip()):
                continue
            if add_period: 
                buffer += "." if buffer[-1] != "." else ""
                add_period = False
            ls = len(final_data)
            # res = re.search("(?<=[^A-Z].[.?]) +(?=[A-Z])", buffer)
            # if debug: print("raw", buffer, res)
            # if res:
            #
            sents = tokenizer.tokenize(buffer)
            if "Speaker series" in buffer:
                print(buffer, sents)
            for s in sents:
                s = s.strip()
                if s[0].isalpha() and s[0].isupper() and s[-1] == ".":
                    final_data.append(s)
                else: buffer_overflow += " " + s
            if debug: print("sents: ", sents)
            # else:
            #     buffer = buffer.strip()
            #     if len(buffer) > 50 and buffer[0].isalpha() and buffer[0].isupper() and buffer[-1] == ".":
            #         final_data.append(buffer)
            #         if debug: print("add", buffer)
            #     else:
            #         buffer_overflow += " " + buffer
            
            buffer = ""
        else:
            if l.isupper(): continue
            orig = l.strip()
            l = re.sub("[^a-zA-Z0-9_'\(\)\.:,’%]+", ' ', l).strip()
            # remove #.#: bullets (verizon)
            l, needs_period = re.subn("^\d+\.\d+:", "", l)
            l = l.strip()
            
            ## CAN MODIFY BULLET POINT STYLE WHITELIST TO ADD/REMOVE
            ## PARSING SUPPORT
            if (orig and orig[0] in ["-", "•", ">"]) or needs_period:
                add_period = True
            buffer += " " + l
    
    
    if parse_overflow:
        # print(buffer_overflow)
        # buffer_overflow = re_punctuate(buffer_overflow)
        sents = tokenizer.tokenize(buffer_overflow) # re.split("(?<=[^A-Z].[.?]) +(?=[A-Z])", buffer_overflow)
        for s in sents:
            s = s.strip()
            if len(s) < 50: continue
            if s[0].isalnum() and s[0].isupper() and s[-1] == ".":
                final_data.append(s)
        print("\n?: ".join(sents))
    if debug: print("\n\n\n===\n", "\n->".join(final_data))
    print("Parsed Lines: ", len(final_data))
    print("Extraction Percentage: ", len(lines)/len(final_data))
    return final_data, buffer_overflow
if __name__ == "__main__":
    ## UNCOMMENT TO DOWNLOAD TOKENIZER:
    nltk.download("punkt")
    final_data = [""]

    # Get the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__+ "/.."))

    # Path to the raw documents folder
    raw_docs_path = os.path.join(script_dir, "raw_docs")

    # Path to the parsed documents folder
    parsed_docs_path = os.path.join(script_dir, "parsed_docs")

    # Create the parsed documents folder if it doesn't exist
    os.makedirs(parsed_docs_path, exist_ok=True)

    # Get a list of PDF files in the raw documents folder
    pdf_files = [f for f in os.listdir(raw_docs_path) if f.endswith(".pdf") and f[:-len(".pdf")]+"_parsed.txt" not in os.listdir(parsed_docs_path)]
    print("Processing: ", pdf_files)
    for pdf_file in pdf_files:
        filename = os.path.splitext(pdf_file)[0]
        # Print log statement for the current file
        print(f"Processing file: {pdf_file}")

        # Parse the PDF file
        esg_report_path = os.path.join(raw_docs_path, pdf_file)
        extracted_text, parse_time = parse_esg_report(esg_report_path)

        # Print log statement for the parsing time
        print(f"Document parsed in {parse_time:.4f} seconds")

        # Save the parsed text to a file
        raw_output_filename = filename + "_raw.txt"
        raw_output_filepath = os.path.join(parsed_docs_path, raw_output_filename)
        with open(raw_output_filepath, 'w', encoding="utf-8") as output_file:
            output_file.write(extracted_text)

        # Open the output file to write the final parsed text
        parsed_output_filepath = os.path.join(parsed_docs_path, filename + "_parsed.txt")
        with open(raw_output_filepath, 'r', encoding="utf-8") as raw_output_file:
            lines = raw_output_file.readlines()  # Read the existing content
            final, _ = pdftext2sents(lines, parse_overflow=False, debug=False)
            with open(parsed_output_filepath, 'w', encoding="utf-8") as out:
                out.writelines("\n\n".join(final))  # Write the final parsed text
                # print("\n\n".join(final))  # Print the final parsed text

        # Print log statement for successful parsing and saving
        print(f"Parsed text written to: {parsed_output_filepath}\n")
