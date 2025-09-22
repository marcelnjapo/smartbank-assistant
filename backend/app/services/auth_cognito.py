# backend/app/services/auth_cognito.py

from jose import JWTError
from jose.jwt import get_unverified_header, decode
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
from ..config import COGNITO_REGION
from ..config import USER_POOL_ID
from ..config import COGNITO_CLIENT_ID

JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json"


security = HTTPBearer()

async def get_public_keys():
    async with httpx.AsyncClient() as client:
        response = await client.get(JWKS_URL)
        response.raise_for_status()
        return response.json()["keys"]

async def verify_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    try:
        public_keys = await get_public_keys()
        headers = get_unverified_header(token)

        # Récupération de la clé publique correspondant au "kid"
        key_data = next(k for k in public_keys if k["kid"] == headers["kid"])

        # Décodage et vérification du JWT
        payload = decode(
            token,
            key=key_data,
            algorithms=["RS256"],
            audience=COGNITO_CLIENT_ID,
            issuer=f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}",
             options={"verify_at_hash": False}
        )

        return payload

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token invalide: {str(e)}")
