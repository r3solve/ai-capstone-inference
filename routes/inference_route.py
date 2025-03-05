from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from meera.inference import GroqModels
from meera.vector_database import MeeraDB

# Define API Router
inference_router = APIRouter(prefix='/v1/inference', tags=['inference'])

# Initialize the Inference Model
groq_endpoint = GroqModels()


class YouTubeModel(BaseModel):
    """
    Model for processing YouTube video inference queries.
    """
    query: str
    namespace: str = Field(
        "",
        description="This is the namespace to search in the vector database. "
                    "Format: `email:[link|doc]:doc_id`",
        title="Search Space"
    )


@inference_router.post("/")
async def youtube_link_inference(
        link: YouTubeModel,
        model_name: str = Query("llama-3.3-70b-versatile", description="AI model name to use for inference.")
):
    """
    📌 **YouTube Video Inference API**

    **Endpoint:** `POST /v1/inference/`

    **Description:**
    - This endpoint allows querying a **YouTube video transcript** stored in the vector database.
    - Uses an **AI model** (default: `llama-3.3-70b-versatile`) for inference.

    ---

    **🔹 Request Parameters (JSON Body)**
    - `query` (string, required) → The question or search query for inference.
    - `namespace` (string, required) → The database namespace storing the video transcript.

    **🔹 Query Parameter**
    - `model_name` (string, optional) → AI model name (default: `"llama-3.3-70b-versatile"`).

    ---

    **📌 Request Example (JSON)**
    ```json
    {
        "query": "What is the main topic of the video?",
        "namespace": "user123:link:789"
    }
    ```

    ---

    **📌 Response Example (Success)**
    ```json
    {
        "response.code": "message succeeded",
        "detail": "The video discusses deep learning techniques."
    }
    ```

    ---

    **📌 Response Example (Error)**
    ```json
    {
        "response.code": "message.error",
        "detail": "Namespace not found in vector database."
    }
    ```

    **Possible Errors**
    - `400 Bad Request` → Invalid request data or missing namespace.
    - `500 Internal Server Error` → AI model failure or vector database error.

    ---

    **🔹 How It Works**
    1. **Retrieves** stored YouTube video transcript embeddings.
    2. **Sends query** to the AI model for context-aware inference.
    3. **Returns the response** with the generated answer.
    """
    try:
        # Retrieve vector embeddings for the given namespace
        meera = MeeraDB(namespace=link.namespace)
        meera_query_response = meera.query_embeddings(link.query)

        # Perform inference using the AI model
        response = await groq_endpoint.infer(
            link.query,
            context=meera_query_response,
            model_name=model_name
        )

        return JSONResponse(
            content={
                "response.code": "message succeeded",
                "detail": str(response),
            }
        )

    except Exception as e:
        return JSONResponse(
            content={
                "response.code": "message.error",
                "detail": str(e)
            },
            status_code=400
        )



@inference_router.get("/models")
async  def list_model_available():
    models = [
        {
            "name": "llama-3.3-70b-versatile",
            "provider": "Meta",
            "context_length": 128000,
            "parameter_size": 32768
        },
        {
            "name": "llama-3.1-8b-instant",
            "provider": "Meta",
            "context_length": 128000,
            "parameter_size": 8192
        },
        {
            "name": "llama-guard-3-8b",
            "provider": "Meta",
            "context_length": 8192,
            "parameter_size": None
        },
        {
            "name": "llama3-70b-8192",
            "provider": "Meta",
            "context_length": 8192,
            "parameter_size": None
        },
        {
            "name": "llama3-8b-8192",
            "provider": "Meta",
            "context_length": 8192,
            "parameter_size": None
        },
        {
            "name": "mixtral-8x7b-32768",
            "provider": "Mistral",
            "context_length": 32768,
            "parameter_size": None
        }
    ]
    return JSONResponse(content=models, status_code=200)