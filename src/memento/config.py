import os
from dataclasses import dataclass, field
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Memento configuration loaded from environment variables."""

    default_provider: str = "openrouter"
    default_model: str = "openai/gpt-4o-mini"
    OPEN_ROUTER_API_KEY: Optional[str] = field(
        default_factory=lambda: os.getenv("OPEN_ROUTER_API_KEY")
    )

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_device: str = "cpu"
    embedding_batch_size: int = 16
    show_progress_bar: bool = False

    PINECONE_API_KEY: Optional[str] = field(
        default_factory=lambda: os.getenv("PINECONE_API_KEY")
    )
    PINECONE_INDEX_NAME: Optional[str] = field(
        default_factory=lambda: os.getenv("PINECONE_INDEX_NAME", "test")
    )
    PINECONE_INDEX_HOST: Optional[str] = field(
        default_factory=lambda: os.getenv("PINECONE_INDEX_HOST")
    )
    PINECONE_NAMESPACE: Optional[str] = field(
        default_factory=lambda: os.getenv("PINECONE_NAMESPACE")
    )

    local_db_path: str = ".memento/memento.db"
    local_index_path: str = ".memento/faiss.index"


config = Config()
