import datetime
import time
from typing import Any

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from jose import jwt
from core.setting import setting


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme.")
            auth_id = self.verify_jwt(credentials.credentials)
            if auth_id is None:
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")
            return auth_id
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def verify_jwt(token: str) -> Any | None:
        try:
            decoded_token = jwt.decode(token, setting.JWT_KEY,
                                       algorithms=[setting.JWT_ALGORITHM])
            now = time.time()
            if decoded_token["expires"] >= now:
                return decoded_token.get("auth_id")
            return None
        except:
            return None


def generate_toke(user_id: str) -> str:
    now = datetime.datetime.utcnow()
    exp = now + datetime.timedelta(minutes=setting.JWT_EXPIRED_MINUTE)
    payload = {
        'id': user_id,
        'exp': exp,
        'iat': now
    }
    token = jwt.encode(payload, setting.JWT_KEY, algorithm=setting.JWT_ALGORITHM)
    return token
