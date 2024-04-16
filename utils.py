import argparse
import shutil


def add_pdf_to_folder(pdf_file, folder):
    if pdf_file.lower().endswith('.pdf'):
        try:
            shutil.copy(pdf_file, folder)
            print(f"Added {pdf_file} to {folder} directory\n")
            return True
        except FileNotFoundError:
            print(f'There is no file named {pdf_file}')
    else:
        print(f"{pdf_file} is not a PDF file")


def load_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf_file', default = None,
                        help="PDF file to add to the folder")
    parser.add_argument('--question', default = None,
                         help="Ask question")
    args = parser.parse_args()
    return args
