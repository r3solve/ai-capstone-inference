import os

from fastapi import FastAPI, APIRouter, File, UploadFile, Query
from fastapi.responses import JSONResponse
from meera.vector_database import MeeraDB
from pydantic import BaseModel, Field
from typing import Any
from meera.chunkers import chunk_long_text
from meera.extractors import  extract_youtube_video_transcript, extract_pdf_content
from models.base_models import YoutubeLinkUploadModel


class YouTubeModel(BaseModel):
    query:str
    namespace:str = Field("",
                          description="This is the namesspace to search in the vector db it's email:[link|doc]:doc_id ",
                          title="Seach Space"
                          )

class FileUploadRequest(BaseModel):
    namespace: str = Field("",
                           description="This is the namesspace to search in the vector db it's email:[link|doc]:doc_id ",
                           title="Seach Space"
                           )


processing_router = APIRouter(prefix="/v1/process", tags= ["files"])


@processing_router.post("/doc")
async  def process_document(file:UploadFile = File(...), namespace:str=Query(...)):
    """
    # Process PDF File and Store Embeddings

    This endpoint allows you to upload a PDF file, extract its text content, and store the extracted content as vector embeddings in the database. The embeddings can later be queried for AI-based inference.

    ---

    ## **Request Method:**
    **POST**

    ## **Endpoint:**
    `/v1/process/doc`

    ---

    ## **Request Parameters:**
    | Parameter  | Type   | Location  | Required | Description  |
    |------------|--------|------------|------------|-------------------------------------------|
    | `namespace` | `string` | Query Parameter | ✅ Yes | The namespace in which the extracted PDF content embeddings will be stored. This helps in organizing and retrieving documents effectively. |

    ---

    ## **Request Body (Multipart Form-Data):**
    | Field | Type | Required | Description |
    |--------|--------|------------|---------------------------------------------------|
    | `file` | `UploadFile` | ✅ Yes | The PDF file to be processed. Only `.pdf` files are allowed. |

    **Example Form-Data Request:**

---

## **Expected Response:**
### **Success Response (`200 OK`)**
```json
{
    "response.code": "operation success",
    "detail": "chunks added to vector db successfully",
    "namespace": "user:doc:12345"
}
"""
    try:
        if not file.filename.endswith(".pdf"):
            return JSONResponse(status_code=400, content={
                "response.code": "operation failed",
                "detail" : "Only PDF files are allowed",
                })

        file_path = f"/tmp/{file.filename}"
        with open(file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        extracted_content = extract_pdf_content(file_path)
        text_chunks = chunk_long_text(extracted_content)
        os.remove(file_path)
        meera = MeeraDB(namespace=namespace)
        meera.upsert_embeddings(text_chunks)
        return JSONResponse(content={
            "response.code":"operation sucesss",
            "detail":"chunks added to vector db successsfull ",
            "namespace":namespace,

        })

    except Exception as e:
        return JSONResponse(content={
            "response.code":"operation failed",
            "detail":str(e)
        }, status_code=400)


@processing_router.post("/link")
async  def process_link(link_data:YoutubeLinkUploadModel):
    """
        Process a YouTube video link and store its transcript embeddings in the vector database.

        **Request Method:** POST
        **Endpoint:** `/v1/process/link`

        **Request Body:**
        ```json
        {
            "source_url": "https://www.youtube.com/watch?v=example",
            "namespace": "user:link:12345"
        }
    """
    try:
        meera = MeeraDB(namespace=link_data.namespace)
        video_content = extract_youtube_video_transcript(link_data.source_url)
        video_content_chunks = chunk_long_text(video_content)
        meera.upsert_embeddings(video_content_chunks)
        return JSONResponse(content={
            "response.code":"operation sucesss",
            "detail":"chunks added to vector db successsfull ",
            "namespace":link_data.namespace
        })
    except Exception as e:
        return JSONResponse(content={
            "response.code":"operation failed",
            "detail":str(e)
        }, status_code=400)
