from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# uvicorn 사용시
if __name__ == "__main__":
    import uvicorn

    # uvicorn을 사용하여 FastAPI 애플리케이션 실행
    uvicorn.run(app, host="127.0.0.1", port=8000)