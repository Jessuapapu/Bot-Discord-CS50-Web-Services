from fastapi import Security, status 

from fastapi.security.api_key import APIKeyHeader
from main import API_KEY    

api_key_header = APIKeyHeader(name="API_KEY", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key inválida o ausente",
        )
