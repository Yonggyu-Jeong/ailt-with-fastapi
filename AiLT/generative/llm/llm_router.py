from fastapi import APIRouter, HTTPException
from generative.llm.llm_service import ask

router_llm = APIRouter()


@router_llm.get('/home' or '/')
def llm_home():
    return {"message": "Hello llm"}


@router_llm.get('/ask/{text}')
def read_user(text: str):
    try:
        return ask(text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
