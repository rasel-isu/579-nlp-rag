from rag.indexing import Indexing
from rag.retrieval import Retriever
from utils import load_arguments


def main():
    args = load_arguments()
    question = args.question
    indexing = Indexing()
    index, nodes = indexing.get_index()
    response = Retriever(index, nodes).get_response(question)
    print(f"\n\n\nResponse : {response}\n\n\n")


if __name__ == "__main__":
    main()
