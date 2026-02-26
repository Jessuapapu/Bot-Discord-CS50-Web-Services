from fastapi import APIRouter, HTTPException, Depends
from Singleton import EstadoGlobal

from utils.apikeyvalidor import get_api_key

SIG = EstadoGlobal.EstadoGlobal()
router = APIRouter()

@router.get("/")
async def obtener_offices():
    return SIG.to_dict()


@router.get("/activas/estudiantes/")
@router.get("/activas/estudiantes/{id_Offices}")
async def obtener_offices(id_Offices: str | None = None):
 
    if id_Offices is not None:
        if  SIG.getOffices(id_Offices) is None:
            return HTTPException(status_code=404,detail="Offices no encontrada")
        
        return SIG.getOffices(id_Offices).to_dictEstudiantes()
    
    return SIG.to_DictActivasEstudiantes()


@router.get("/activas/informacion/")
async def obtener_officesInformacion():  
    return SIG.to_DictInformacion()


@router.get("/get/{id_Offices}")
async def obtener_officesEsoecifica(id_Offices: str):
    return SIG.getOffices(id_Offices).to_dict() if SIG.getOffices(id_Offices) is not None else HTTPException(status_code=404,detail="Offices no encontrada")

