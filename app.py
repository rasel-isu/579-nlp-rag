import os
import time
import traceback
from typing import List
import IPython
import fitz
import ipywidgets
import funix
from funix.widget.builtin import BytesFile
from rag.indexing import Indexing
from rag.retrieval import Retriever


@funix.funix(
        title="RAG",
        theme="./kanagawa.json",
        print_to_web=True,
        description="Provide your OpenAI API token and pdf file, then ask a question",
        widgets={
         "question": "textarea"
        })
def get_result(
               openai_key: ipywidgets.Password,
               filepaths: List[BytesFile],
               question: str = "",
               ) -> IPython.display.Markdown:

    os.environ["OPENAI_API_KEY"] = openai_key.value

    try:
        texts = []
        for i, file in enumerate(filepaths):
            with fitz.open(stream=file, filetype="pdf") as doc:
                text_list = [page.get_text() for page in doc]
                texts+=text_list

        indexing = Indexing(texts)
        index, nodes = indexing.get_index()
        response = Retriever(index, nodes).get_response(question)

        yield '<h1>Answer:</h1><br><div style="text-align:justify;background-color:#f7e4bc;color:black;padding:10px;"><i>'
        for i in response.split(' '):
            time.sleep(0.05)
            yield i
        yield '</i></div>'

    except Exception as e:
        print(str(traceback.format_exc()))

    os.environ["OPENAI_API_KEY"] = ''

    return None
