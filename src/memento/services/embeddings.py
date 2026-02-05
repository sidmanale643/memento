from memento.config import config
from sentence_transformers import SentenceTransformer

class EmbeddingsFactory:
    def __init__(self):
        
        self.model = SentenceTransformer(
            config.embedding_model,
            device=config.embedding_device
        )
    
    def embed(self, sentences):

        embeddings = self.model.encode(
            sentences=sentences,
            show_progress_bar=config.show_progress_bar,
            batch_size=config.embedding_batch_size
        )

        return embeddings
