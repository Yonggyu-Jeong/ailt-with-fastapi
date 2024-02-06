from fastapi import APIRouter, HTTPException

from generative.llm.llm_service import ask

router_llm = APIRouter()


@router_llm.get('/')
def llm_home():
    return {"message": "Hello llm"}


@router_llm.get('/ask')
def llm_ask(text: str):
    try:
        text = "건강하게 살기 위한 세 가지 방법은?"
        return ask(text)


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
