from fastapi import FastAPI
from fastapi.responses import  JSONResponse
from routes.inference_route import  inference_router
from routes.processing_route import processing_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Infrence Routes",
              description="This gateway is for interecting with the internal inference engine"
              )

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async  def home_route():
    """
    **Params:
        None

    :return:
        {message:"welcome to the api"}
    """
    return JSONResponse(content={"message":"welcome to the api"},
                        status_code=200)
all_routes = [inference_router, processing_router]
for router in all_routes:
    app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8080, reload=True)