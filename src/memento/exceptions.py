
class MementoError(Exception):
    def __init__(self, message: str, details: dict):
        super().__init__(message)

        self.message = message
        self.details = details or {}
    
class StorageError(MementoError):
    pass

class SummarisationError(MementoError):
    pass

class ExtractionError(MementoError):
    pass

class IndexError(MementoError):
    pass

class LlmError(MementoError):
    pass

class StyleError(MementoError):
    pass