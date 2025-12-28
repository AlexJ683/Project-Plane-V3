from fastapi import FastAPI, HTTPException, Depends, status, Query
from pydantic import BaseModel
from typing import Annotated, List, Optional
from utils import models
from utils.database import engine, SessionLocal
from sqlalchemy.orm import Session
import uvicorn

app = FastAPI()

class PostBase(BaseModel):
    airline: str
    flight_number: str
    departure_city: str
    departure_time: str
    stops: int
    arrival_time: str
    arrival_city: str
    travel_class: str
    duration: str
    days_left: int
    price: int


def get_db():
    # create a method of db but no matter what happens it will close the db connection
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dep = Annotated[Session, Depends(get_db)]

@app.get("/all_items/", status_code=status.HTTP_200_OK)
async def get_all_items(db: db_dep):
    db_posts = db.query(models.flights).all()
    if db_posts is None:
        raise HTTPException(status_code=404, detail="flight not found")
    return db_posts


@app.get("/posts/{flight_id}", status_code=status.HTTP_200_OK)
async def read_post(flight_id: int, db: db_dep):
    db_post = db.query(models.flights).filter(models.flights.id == flight_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="flight not found")
    return db_post

@app.delete("/posts/{flight_id}", status_code=status.HTTP_200_OK)
async def delete_post(flight_id: int, db: db_dep):
    db_post = db.query(models.flights).filter(models.flights.id == flight_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="flight not found")
    db.delete(db_post)
    db.commit()
    return {"detail": "Post deleted"}

@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dep):
    db_post = models.flights(**post.dict())
    db.add(db_post)
    db.commit()

@app.get("/")
def root():
    return {"status": "ok"}


if __name__ == "__main__":
    
    models.Base.metadata.create_all(bind=engine)
    uvicorn.run(app, port=8000, host="0.0.0.0")


