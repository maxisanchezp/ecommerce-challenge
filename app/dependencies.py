from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

from app.models import SessionLocal, User, ApiKey


# JWT Config

SECRET_KEY = 'secret-key-clt-prueba'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# DB DEPENDENCY
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API KEY Auth

def get_api_key(x_api_key: str = Header(...), db: Session = Depends(get_db)):
    api_key = db.query(ApiKey).filter(ApiKey.key == x_api_key, ApiKey.active).first()
    if not api_key:
        raise HTTPException(status_code=403, detail="Missing or Invalid API KEY")
    


# JWT FUNCTIONS

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Header(...), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail="Couldn't validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user