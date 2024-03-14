import os
from dotenv import load_dotenv,find_dotenv
import weaviate
from llama_index.core.node_parser import SentenceWindowNodeParser
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, \
    StorageContext
from llama_index.core.indices.loading import load_index_from_storage
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.settings import Settings
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from config import DIR_INDEX, DIR_PDF, INDEX_NAME


load_dotenv(find_dotenv()) 

class Indexing:

    def __init__(self) -> None:
       # model = 'BAAI/bge-m3'
        # model = 'Salesforce/SFR-Embedding-Mistral'
        # model = 'BAAI/bge-m3'
        # model = 'sentence-transformers/all-MiniLM-L6-v2'
        # Settings.llm =HuggingFaceLLM(
        #     generate_kwargs={"temperature": 0.1, "do_sample": False},
        #     tokenizer_name=model,
        #     model_name=model,
        #     device_map="cpu",
        # )
        # Settings.embed_model =  HuggingFaceEmbedding(model_name=model)
        Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
        Settings.embed_model = OpenAIEmbedding()

    def get_all_pdf(self):
        files = []

        for i in os.listdir(DIR_PDF):
            files.append(f'{DIR_PDF}/{i}')
        return files


    def load_documents(self):
        files = self.get_all_pdf()
        documents = SimpleDirectoryReader(
                input_files=files
        ).load_data()
        return documents
    
    def get_nodes(self):
        documents = self.load_documents()
        node_parser = SentenceWindowNodeParser.from_defaults(
        window_size=3,
        window_metadata_key="window",
        original_text_metadata_key="original_text",)
        nodes = node_parser.get_nodes_from_documents(documents)
        return nodes
    
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
        
