from fastapi import FastAPI, Depends, HTTPException, Form
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from datetime import timedelta
from passlib.context import CryptContext

import crud
import models 
import schemas
from models import SessionLocal, engine, User
from message_queue import publish_order_message
from external import get_external_product
from dependencies import (
    get_current_user,
    get_api_key,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


def init_db():
    models.Base.metadata.create_all(bind=engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


# Dependencia para obtener DB


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@app.post("/auth/login")
def login(
    username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=401, detail="Incorrect username or password, Try Again!"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/secure-data")
def secure_data(api_key=Depends(get_api_key)):
    return {"message": "You accessed this with a valid API KEY!"}


@app.get("/me")
def read_user_me(current_user: User = Depends(get_current_user)):
    return {"message": current_user.username, "email": current_user.email}

@app.post("/orders", response_model=schemas.OrderRead)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        db_order = crud.create_order(db, order)
        publish_order_message(db_order.id, db_order.total_amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_order


@app.get("/orders/{order_id}", response_model=schemas.OrderRead)
def read_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_order = crud.get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order NOT Found")
    return db_order


@app.get("/products/{product_id}", response_model=schemas.ProductRead)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product NOT Found")
    return db_product


@app.get("/external-products/{product_id}")
async def read_external_product(product_id: int):
    external_product = await get_external_product(product_id)
    return external_product


if __name__ == "__main__":
    import uvicorn

    init_db()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
