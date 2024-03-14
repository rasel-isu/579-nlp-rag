from copy import deepcopy
from llama_index.core.postprocessor import MetadataReplacementPostProcessor
from llama_index.core.postprocessor import SentenceTransformerRerank


class Retriever:

    def __init__(self, index, nodes) -> None:
        self.index, self.nodes = index, nodes
        self.postproc = MetadataReplacementPostProcessor(target_metadata_key="window")
        # BAAI/bge-reranker-base
        # link: https://huggingface.co/BAAI/bge-reranker-base
        self.model_reranker = "BAAI/bge-reranker-base"
        # model_reranker = model
        self.rerank = SentenceTransformerRerank(top_n = 2, model = self.model_reranker)

    def get_response(self, query):
        query_engine = self.index.as_query_engine(
            similarity_top_k = 6,
            vector_store_query_mode="hybrid",
            alpha=0.5,
            node_postprocessors = [self.postproc, self.rerank],
        )
        response = query_engine.query(query)
        return str(response)