import os
import json
import tiktoken
from bs4 import BeautifulSoup
from dotenv import load_dotenv,find_dotenv
import weaviate
from llama_index.core.node_parser import SentenceWindowNodeParser, SentenceSplitter
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, \
    StorageContext, Document
from llama_index.core.indices.loading import load_index_from_storage
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.settings import Settings
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from config import DIR_INDEX, DIR_PDF, INDEX_NAME


# load_dotenv(find_dotenv())

class TextCleaner:

    def __init__(self, text):
        self.text = text

    def remove_page_number_from_pdf(self):
        pass

    def remove_html_tags(self):
        soup = BeautifulSoup(self.text, 'html.parser')
        clean_text = soup.get_text()
        return clean_text

    def clean(self):
        text =  self.remove_html_tags()
        return text
class Indexing:

    def __init__(self, texts=[]) -> None:
       self.texts = texts
       self.model_name = "gpt-3.5-turbo"
       Settings.text_splitter = SentenceSplitter(
           separator=" ", chunk_size=200, chunk_overlap=50,
           paragraph_separator="\n\n\n",
           secondary_chunking_regex="[^,.;。]+[,.;。]?",
           tokenizer=tiktoken.encoding_for_model(self.model_name).encode
       )
       Settings.llm = OpenAI(model=self.model_name, temperature=0.1)
       Settings.embed_model = OpenAIEmbedding()

    def load_documents(self):
        documents = []
        if self.texts:
            for doc in self.texts:
                clean_text = TextCleaner(doc).clean()
                documents.append(Document(text=clean_text))
        else:
            files = self.get_all_pdf()
            reader = SimpleDirectoryReader(
                input_files=files
            )
            for docs in reader.iter_data():
                for doc in docs:
                    clean_text = TextCleaner(doc.text).clean()
                    doc.text = clean_text
                    documents.append(doc)
        return documents

    def get_all_pdf(self):
        files = []

        for i in os.listdir(DIR_PDF):
            files.append(f'{DIR_PDF}/{i}')
        return files
    
    def get_nodes(self):
        documents = self.load_documents()
        node_parser = SentenceWindowNodeParser.from_defaults(
        window_size=3,
        window_metadata_key="window",
        original_text_metadata_key="original_text",)
        nodes = node_parser.get_nodes_from_documents(documents)
        return nodes
    
    def save_data_from_index_to_file(self, client):

        response = client.data_object.get(
            class_name=INDEX_NAME,
            with_vector=True)

        with open("index_data.json","w") as f:
            json.dump(response, f, indent=2)

    def get_index(self):
        
        client = weaviate.Client(
            embedded_options=weaviate.embedded.EmbeddedOptions()
            
        )
        vector_store = WeaviateVectorStore(
            weaviate_client = client,
            index_name = INDEX_NAME
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        if client.schema.exists(INDEX_NAME):
            client.schema.delete_class(INDEX_NAME)
        nodes = self.get_nodes()
        index = VectorStoreIndex(
            nodes,
            storage_context = storage_context,
        )
        
        self.save_data_from_index_to_file(client)

        return index, nodes
    
    # def save_index(self):
    #     index = self.get_index()
    #     index.storage_context.persist(DIR_INDEX)

    def load_index(self):
        client = weaviate.Client(
            embedded_options=weaviate.embedded.EmbeddedOptions(),
        )
        vector_store = WeaviateVectorStore(
            weaviate_client = client,
            index_name = INDEX_NAME
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_vector_store(
            vector_store, storage_context=storage_context)
        return index
        
