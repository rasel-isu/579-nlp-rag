# 579-NLP-RAG
## Installation
```pip install -r requirements.txt```

### Command Line

#### How to upload PDF?

```python upload.py --pdf_file=example.pdf```

 [Video](www.google.com)

#### Ask your question to the RAG

```python query.py --question="What is the meaning of life?"```

### GUI

[Video](www.google.com)


### Export data from vectorDB
```self.save_data_from_index_to_file(client)```  

**File** : *index_data.json*

## Steps in Code
- Upload/Add PDF to RAG

    ```is_added = add_pdf_to_folder(pdf_file, folder)```    

- Ingest : removed HTML

    ```clean_text = TextCleaner(doc.text).clean()```
- Chunking :
    ```
  Settings.text_splitter = SentenceSplitter(
           separator=" ", chunk_size=200, chunk_overlap=50,
           paragraph_separator="\n\n\n",
           secondary_chunking_regex="[^,.;。]+[,.;。]?",
           tokenizer=tiktoken.encoding_for_model(self.model_name).encode
  )
  ```
- Embed the chunks
  
  ```index, nodes = indexing.get_index()```

- Rerank:

    ```self.rerank = SentenceTransformerRerank(top_n = 5, model = self.model_reranker)```
 
- Retrieval:
   ```
  query_engine = self.index.as_query_engine(
            similarity_top_k = 5,
            vector_store_query_mode="hybrid",
            alpha=0.5,
            node_postprocessors = [self.postproc, self.rerank],
        )
  ```
- Generate:

    ```response = Retriever(index, nodes).get_response("What is t5?")```



  
  