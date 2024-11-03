from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_function():
    model_path = "sentence-transformers/all-MiniLM-L6-v2"  
    model_kwargs = {'device': 'cpu'} 
    
    embeddings = HuggingFaceEmbeddings(model_name=model_path, model_kwargs=model_kwargs)
    return embeddings
