"""Memory record data model."""

from time import time
from typing import Any, Dict, List, Literal, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class MemoryRecord(BaseModel):
    """A single memory record stored by Memento."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    text: str
    memory_type: Literal["fact", "preference", "task", "note", "summary"] = "note"
    style: Literal["claude", "chatgpt", "memo"] = "claude"
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None
    created_at: float = Field(default_factory=time)
    expires_at: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    embedding: Optional[List[float]] = None

    def is_expired(self) -> bool:
        """Check if this memory has expired."""
        if self.expires_at is None:
            return False
        
        return time() > self.expires_at

    def to_vector_dict(self) -> dict:
        """Convert to dict format for vector DB upsert."""
        metadata = {
            "text": self.text,
            "memory_type": self.memory_type,
            "style": self.style,
            "created_at": self.created_at,
            **self.metadata,
        }
        
        # Only add optional fields if they have values (Pinecone doesn't accept nulls)
        if self.user_id is not None:
            metadata["user_id"] = self.user_id
        if self.conversation_id is not None:
            metadata["conversation_id"] = self.conversation_id
        if self.expires_at is not None:
            metadata["expires_at"] = self.expires_at
        
        return {
            "id": self.id,
            "values": self.embedding,
            "metadata": metadata,
        }

    @classmethod
    def from_vector_match(cls, match: dict) -> "MemoryRecord":
        """Create a MemoryRecord from a vector DB query result."""
        metadata = match.get("metadata", {})
        return cls(
            id=match.get("id", str(uuid4())),
            text=metadata.pop("text", ""),
            memory_type=metadata.pop("memory_type", "note"),
            style=metadata.pop("style", "claude"),
            user_id=metadata.pop("user_id", None),
            conversation_id=metadata.pop("conversation_id", None),
            created_at=metadata.pop("created_at", time()),
            expires_at=metadata.pop("expires_at", None),
            metadata=metadata,
            embedding=match.get("values"),
        )
