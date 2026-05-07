from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from config import ETHOS_API_KEY

API_KEY_NAME = "X-Ethos-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(
    api_key_header: str = Security(api_key_header),
):
    if api_key_header == ETHOS_API_KEY:
        return api_key_header
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
    )
