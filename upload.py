import os

from config import DIR_PDF
from rag.indexing import Indexing
from rag.retrieval import Retriever
from utils import add_pdf_to_folder, load_arguments


def main():

    args = load_arguments()
    pdf_file = args.pdf_file
    folder = DIR_PDF

    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    is_added = add_pdf_to_folder(pdf_file, folder)
    if is_added:
        indexing = Indexing()
        index, nodes = indexing.get_index()
        response = Retriever(index, nodes).get_response("What is t5?")
        print(f"\n\n\nResponse : {response}\n\n\n")


if __name__ == "__main__":
    main()
