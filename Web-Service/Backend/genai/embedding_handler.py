from pinecone import Pinecone
import openai
import os
pc = Pinecone(
        api_key=os.getenv('pinecone_key')
    )

openai.api_key = os.getenv('openai_key')

def generate_embedding(text_to_embed):
    model_name = "text-embedding-3-small"
    response = openai.embeddings.create(
        model=model_name,
        input=text_to_embed,
        encoding_format="float"  # Adjust format if needed (e.g., "json")
    )
    # embedding_vector = np.array(base64.b64decode(response.data[0].embedding))
    return response.data[0].embedding if len(response.data)>0 else None
def retrieve_products(prompt,category,k=5):
    """
    Function to retrieve relevant product information from Pinecone.
    """

    query_vectors = generate_embedding(prompt)
    if not query_vectors:
        return []
    index = pc.Index('marketplace')
    results = index.query(vector=query_vectors, top_k=k,
                               namespace=category, include_values=True,
                               include_metadata=True
                               )
    unique_products = {}
    for result in results['matches']:
        asin = result['metadata']['asin']
        summary = result['metadata']['summary']
        unique_products[asin] = summary
    
    # Convert the dictionary values to a list
    products = [{"asin": asin, "summary": summary} for asin, summary in unique_products.items()]
    
    return products
