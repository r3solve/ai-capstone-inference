from pydantic import BaseModel

class YoutubeLinkUploadModel(BaseModel):
    source_url:str
    namespace:str

class DocumentUploadModel(BaseModel):
    pass