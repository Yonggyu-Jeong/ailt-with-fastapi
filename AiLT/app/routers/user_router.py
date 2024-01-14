from fastapi import APIRouter

router = APIRouter()

@Controller

@router.get("/user")
async def user():
    return {"message": "Hello World"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

