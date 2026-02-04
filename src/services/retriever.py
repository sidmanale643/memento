from typing import Any, Iterable, List, Optional
from pinecone import Pinecone
from src.config import config


class Retriever:
    def __init__(self):
        
        self.api_key = config.PINECONE_API_KEY
        
        if not self.api_key:
            raise ValueError("PINECONE_API_KEY is required to use Pinecone.")

        self.index_name = config.PINECONE_INDEX_NAME 
        self.index_host = config.PINECONE_INDEX_HOST
        self.namespace = config.PINECONE_NAMESPACE

        pc = Pinecone(api_key=self.api_key)

        if self.index_host:
            self.index = pc.Index(host=self.index_host)
        elif self.index_name:
            self.index = pc.Index(self.index_name)
        else:
            raise ValueError(
                "Set PINECONE_INDEX_HOST or PINECONE_INDEX_NAME to target an index."
            )

    def upsert(
        self,
        vectors: Iterable[dict[str, Any]],
        namespace: Optional[str] = None,
    ):
        ns = namespace or self.namespace
        return self.index.upsert(vectors=vectors, namespace=ns)

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
