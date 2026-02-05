from typing import Any, Iterable, List, Optional
from pinecone import Pinecone, ServerlessSpec
from memento.config import config

class Retriever:
    def __init__(self):
        
        self.api_key = config.PINECONE_API_KEY
        
        if not self.api_key:
            raise ValueError("PINECONE_API_KEY is required to use Pinecone.")

        self.index_name = config.PINECONE_INDEX_NAME
        self.index_host = config.PINECONE_INDEX_HOST
        self.namespace = config.PINECONE_NAMESPACE

        pc = Pinecone(api_key=self.api_key)
        
        if not self.index_name:
            raise ValueError("PINECONE_INDEX_NAME is required.")
            
        if not pc.has_index(self.index_name):
            
            print(f"Index '{self.index_name}' does not exist. Creating with dimension 384...")
            pc.create_index(
                name=self.index_name,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            print(f"Index '{self.index_name}' created successfully!")
        
        self.index = pc.Index(self.index_name)

    def upsert(
        self,
        records: Iterable[dict[str, Any]],
        namespace: Optional[str] = None,
    ):
        ns = namespace or self.namespace
        return self.index.upsert(vectors=list(records), namespace=ns)

    def query(
        self,
        vector: List[float],
        top_k: int = 5,
        namespace: Optional[str] = None,
        filter: Optional[dict[str, Any]] = None,
        include_metadata: bool = True,
        include_values: bool = False,
    ):
        ns = namespace or self.namespace
        
        return self.index.query(
            vector=vector,
            top_k=top_k,
            namespace=ns,
            filter=filter,
            include_metadata=include_metadata,
            include_values=include_values,
        )

    def retrieve(
        self,
        vector: List[float],
        top_k: int = 5,
        namespace: Optional[str] = None,
        filter: Optional[dict[str, Any]] = None,
    ):
        return self.query(
            vector=vector,
            top_k=top_k,
            namespace=namespace,
            filter=filter,
            include_metadata=True,
            include_values=False,
        )