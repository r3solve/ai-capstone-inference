
class MeeraException(Exception):
    def __init__(self, message:str):
        super().__init__(message)


class VectorInsertException(MeeraException):
    def __init__(self,message:str="failed to insert embeddings"):
        super().__init__(message)

class EmbeddingsException(MeeraException):
    def __init__(self,message:str="failed to generate embeddings"):
        super().__init__(message)
        
class EmbeddingsQueryException(MeeraException):
    def __init__(self, message:str="query failed"):
        super().__init__(message)