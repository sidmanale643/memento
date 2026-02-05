# Memento

A memory management system for AI/LLM applications with semantic retrieval and summarization capabilities.

## Overview

Memento provides a flexible memory layer for AI agents and applications, supporting multiple memory styles (Claude, ChatGPT, Mem0), vector-based retrieval using Pinecone, and LLM-powered summarization and extraction.

## Features

- **Memory Styles**: Support for Claude, ChatGPT, and Mem0-style memory extraction
- **Vector Retrieval**: Semantic search using Pinecone vector database
- **LLM Integration**: Powered by OpenRouter for summarization and extraction
- **Embedding Support**: Uses sentence-transformers for text embeddings
- **Flexible Storage**: Pydantic-based memory records with metadata support
- **TTL Support**: Optional expiration for time-sensitive memories

## Installation

This project uses Python 3.11+ and `uv` for package management.

```bash
# Clone the repository
git clone <repo-url>
cd memento

# Install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate
```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# LLM Configuration
OPEN_ROUTER_API_KEY=your_openrouter_api_key

# Vector Database (Pinecone)
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_index_name
PINECONE_INDEX_HOST=your_index_host
PINECONE_NAMESPACE=default
```

## Quick Start

```python
from src.memento.memento import Memento
from src.memento.services.llm import LlmFactory
from src.memento.services.retriever import Retriever

# Initialize Memento with your preferred style
memento = Memento(style="claude")

# Use LLM for summarization
llm = LlmFactory()
summary = llm.summarise("Long text to summarize...")

# Store and retrieve memories
retriever = Retriever()
# Memories are automatically upserted to Pinecone
```

## Project Structure

```
memento/
├── main.py                      # CLI entry point
├── src/memento/
│   ├── config.py               # Environment configuration
│   ├── memento.py              # Main orchestration class
│   ├── exceptions.py           # Custom exceptions
│   ├── models/
│   │   └── record.py           # MemoryRecord Pydantic model
│   ├── services/
│   │   ├── llm.py              # LLM client (LlmFactory)
│   │   ├── embeddings.py       # Embeddings generation
│   │   ├── retriever.py        # Vector DB retrieval
│   │   └── prompts.py          # LLM prompts
│   ├── stores/
│   │   └── base.py             # Storage interface
│   └── styles/
│       ├── base.py             # Base style class
│       ├── claude.py           # Claude memory style
│       ├── chatgpt.py          # ChatGPT memory style
│       ├── memo.py             # Mem0 style
│       └── utils.py            # Style utilities
├── pyproject.toml              # Project dependencies
└── uv.lock                     # Locked dependencies
```

## Usage

### Creating Memory Records

```python
from src.memento.models.record import MemoryRecord

record = MemoryRecord(
    text="User prefers dark mode",
    memory_type="preference",
    style="claude",
    user_id="user_123",
    metadata={"source": "settings"}
)
```

### Retrieving Memories

```python
from src.memento.services.embeddings import EmbeddingsFactory
from src.memento.services.retriever import Retriever

# Generate embeddings
embedder = EmbeddingsFactory()
embedding = embedder.encode(["query text"])

# Search vector database
retriever = Retriever()
results = retriever.retrieve(
    vector=embedding[0],
    top_k=5,
    filter={"memory_type": "preference"}
)
```

### Summarization

```python
from src.memento.services.llm import LlmFactory

llm = LlmFactory()
summary = llm.summarise(long_conversation_text)
extracted_facts = llm.extract(text_to_analyze)
```

## Development

### Running Tests

```bash
# Install test dependencies
uv add --dev pytest pytest-cov

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/memento tests/
```

### Code Quality

```bash
# Install linting tools
uv add --dev ruff black mypy

# Check code style
uv run ruff check src/

# Format code
uv run black src/

# Type checking
uv run mypy src/memento
```

## Dependencies

- **Python**: 3.11+
- **LLM**: OpenAI client with OpenRouter support
- **Vector DB**: Pinecone
- **Embeddings**: sentence-transformers
- **Validation**: Pydantic
- **Package Manager**: uv

## License

[Add your license here]

## Contributing

[Add contribution guidelines]
