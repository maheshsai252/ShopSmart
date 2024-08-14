from pinecone import Pinecone, ServerlessSpec
import os
import openai
import requests
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
openai.api_key = os.getenv('openai_key')
pc = Pinecone(
        api_key=os.getenv('pinecone_key')
    )

def store_in_pinecone(embeddings, chunk_ids, meta, namespace):
    index_name = "marketplace"
    index = pc.Index(index_name)
  
    index.upsert(vectors=list(zip(chunk_ids, embeddings,meta)), namespace=namespace)

def store_images_in_pinecone(embeddings, chunk_ids, meta, namespace):
    index_name = "marketplace-images"

    index = pc.Index(index_name)
    
    index.upsert(vectors=list(zip(chunk_ids, embeddings,meta)), namespace=namespace)

def generate_embedding(text_to_embed):
    model_name = "text-embedding-3-small"

    response = openai.embeddings.create(
        model=model_name,
        input=text_to_embed,
        encoding_format="float"  # Adjust format if needed (e.g., "json")
    )
    # embedding_vector = np.array(base64.b64decode(response.data[0].embedding))
    return response.data[0].embedding

