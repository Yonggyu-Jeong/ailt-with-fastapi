import uvicorn
from fastapi import FastAPI
from app.image import image_router
#from app.llm import llm_router

#DOKER 분리용

app = FastAPI()

#app.include_router(llm_router.router_llm, prefix="/llm", tags=["llm"])
app.include_router(image_router.router_image, prefix="/image", tags=["image"])


@app.get("/")
async def root():
    return {"message": "Hello app solution"}


# uvicorn 사용하여 FastAPI 실행
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
