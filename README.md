# Retrieval-augmented generation (RAG)
### Test our hosted application
http://138.2.71.205:3000/

## Build and run using docker
```docker-compose up --build -d```

### localhost : http://0.0.0.0:3000/

<a href="" target="_blank">Video!</a>

## Install locally
[_**Important Note : Don't run on Windows because it does not supported with Embedded DB!**_
](https://github.com/weaviate/weaviate/issues/3315)


Linux

```pip3 install -r requirements.txt```

Mac

```python3 -m pip install --upgrade pip```

```pip3 install -r requirements_mac.txt```

#### Create a .env file in the root folder, put the line below and replace YOUR_API_KER with your openai api key
```OPENAI_API_KEY=YOUR_API_KER```

### Command Line

#### How to upload PDF?

```python upload.py --pdf_file=mt5.pdf```

<a href="https://youtu.be/z_Xjxqk8E4g" target="_blank">Video!</a>
#### Ask your question to the RAG

```python query.py --question="What is mt5?"```

<a href="https://youtu.be/H8mwEB64cJ0" target="_blank">Video!</a>
### GUI

<a href="" target="_blank">Video!</a>


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


