from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    
    #LLM Service
    default_provider= "openrouter"
    default_model = "openai/gpt-5-nano"
    OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY", None)

    #Embedding Service
    default_embedding_model= "sentence-transformers/all-MiniLM-L6-v2"
    device= "cpu"
    show_progress_bar= True
    batch_size= 16
    
    #Pinecone Service
    PINECONE_API_KEY= os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME= os.getenv("PINECONE_INDEX_NAME")
    PINECONE_INDEX_HOST= os.getenv("PINECONE_INDEX_HOST")
    PINECONE_NAMESPACE= os.getenv("PINECONE_NAMESPACE")

    #DB Service
    
    #Neo4J Service

config = Config()
