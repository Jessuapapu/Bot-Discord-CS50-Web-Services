from fastapi import APIRouter, HTTPException, Depends
from Singleton import EstadoGlobal

from utils.apikeyvalidor import get_api_key

SIG = EstadoGlobal.EstadoGlobal()
router = APIRouter()


#@router.post("/")
#async def 