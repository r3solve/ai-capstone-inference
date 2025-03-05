
from fastapi import APIRouter, HTTPException, Query, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from  meera.inference import GroqModels
from meera.extractors import extract_youtube_video_transcript
from meera.chunkers import  chunk_long_text
from meera.vector_database import MeeraDB
from models.base_models import YoutubeLinkUploadModel


inference_router = APIRouter(prefix='/v1/inference')

groq_endpoint = GroqModels()
class YouTubeModel(BaseModel):

    query:str
    namespace:str = Field("",
                          description="This is the namesspace to search in the vector db \ it's email:[link|doc]:doc_id ",
                          title="Seach Space"
                          )


@inference_router.post("/link/process", description="process link for inference")
async  def process_document(link_data:YoutubeLinkUploadModel):
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

@inference_router.post("/doc/process",
                       description="process documents for inference")
async def process_document_files(file:UploadFile = File(...)):
    try:

        return JSONResponse(content={
            "response.code":"operation sucesss",
            "namespace":"example-namespace",
            "detail":"operation completed"
        })
    except Exception as e:
        return  JSONResponse(content={
            "response.code":"operation failed",
            "detail":"operation could not complete"
        }, status_code=400)

@inference_router.post("/")
async  def youtube_link_inference(link:YouTubeModel,
                                  model_name:str = Query("llama-3.3-70b-versatile")):
    """
     Send inference requests through this enpoint by passing the video data
    :param link:
    :param model_name:
    :return:
        {
            "response.status" : "message sucessfull" | "message error",
            "detail" : "detail reponse"
        }
    """
    try:
        meera = MeeraDB(namespace=link.namespace)
        meera_query_response = meera.query_embeddings(link.query)
        response = groq_endpoint.infer(link.query, context=meera_query_response, model_name=model_name)

        return JSONResponse(content={
            "response.code":"message succeeded",
            "detail":str(response),
        })
    except Exception as e:
        return JSONResponse(content={"response.code":"message.error",
                                     "detail": str(e)
                                     },
                            status_code=400
                            )