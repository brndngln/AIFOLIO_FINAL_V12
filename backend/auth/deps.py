from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from backend.main import oauth2_scheme
from backend.config.settings import SECRET_KEY, ALGORITHM, SECRET_USERNAME


from typing import Dict

def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role", "admin")
        email: str = payload.get("email", None)
        org: str = payload.get("org", None)
        if username != SECRET_USERNAME:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"username": username, "role": role, "email": email, "org": org}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
