"""
import uvicorn
from fastapi import FastAPI
#from generative.image import image_router
from generative.llm import llm_router

#DOKER 분리용

app = FastAPI()

app.include_router(llm_router.router_llm, prefix="/llm", tags=["llm"])


@app.get("/")
async def root():
    return {"message": "Hello generative solution"}


# uvicorn 사용하여 FastAPI 실행
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

"""