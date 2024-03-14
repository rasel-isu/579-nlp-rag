import argparse
import shutil
import os

from config import DIR_PDF
from rag.indexing import Indexing

def add_pdf_to_folder(pdf_file, folder):
    if pdf_file.lower().endswith('.pdf'):
        try:
            shutil.copy(pdf_file, folder)
            print(f"Added {pdf_file} to {folder}")
            return True
        except FileNotFoundError:
            print(f'There is no file named {pdf_file}')
    else:
        print(f"{pdf_file} is not a PDF file")

def load_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf_file',
                         help="PDF file to add to the folder")
    args = parser.parse_args()
    return args


def main():

    args = load_arguments()
    pdf_file = args.pdf_file
    folder = DIR_PDF

    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    is_added = add_pdf_to_folder(pdf_file, folder)
    if is_added:
        indexing = Indexing()
        indexing.save_index()
        index = indexing.load_index()
        new_query_engine = index.as_query_engine()
        response = new_query_engine.query("who is this text about?")
        print(response)


if __name__ == "__main__":
    main()
