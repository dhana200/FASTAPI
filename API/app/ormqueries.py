from typing import Optional
from fastapi import Depends, FastAPI  ### Importing FastAPI from fastapi library
from fastapi.params import Body ### Body parameter is used to get data from the user's input
from pydantic import BaseModel ### Importing pydantic model
from random import randrange  ### To provide randome integer in bteween some specified range
from fastapi import Response,status ### To validate the response to send it to front end of the user and status of the query
from fastapi import HTTPException ### To raise http exceptions while performing any path operations
import psycopg2 ### To Connect to postgres instance
from psycopg2.extras import RealDictCursor ### This is to retrive the values with column names in dictionary format
import time ### To use time functions
from . import models,Schemas
from sqlalchemy.orm import Session
from .database import SessionLocal, engine,get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):    # Anytime databse usage is required this path operation is mandatory step
    # This command helps to collect all the data from the respective table 
    # In this function query function gets the data from the table in which it is stored 
    # without all() function it's just a sql code
    posts = db.query(models.Post).all() 
    return posts

@app.post("/posts",status_code=status.HTTP_201_CREATED,response_class=Schemas.Post)
def create_posts(post: Schemas.PostCreate, db : Session = Depends(get_db)):
    # To create a post and publish it into database
    # models.post("post parameter/variable") take all the paramenters required for the data entry (mandatory fields)
    # to publish the data provided by the user into database is 2 steps to follow 1. db.add("post parameter/variable"), 2.commit
    # to retrive the data from the database which is created from the user input using db.refresh("passing a parameter")
    #This method of getting data is valid but will be exhausting for the large and big data places.
    # new_posts = models.Post(title = post.title, content=post.Contents, published = post.published)
    # Instead we convert all the data into dictionary and send it to the  **post.dict()
    # ** before post.dict() unpacks all the data in a single line format which is basically enlongating 
    new_post = models.Post(**post.dict())  
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}",status_code=status.HTTP_302_FOUND)
def get_post(id: int, db:Session = Depends(get_db)):
    # To fetch a single respective post
    # to fetch the repective post we make use of filter which basically like where condition in SQL 
    # after filtering out the we need to retrive. 
    # for doing this we can make use of all() function but this all() function doesn't stop with one entry it will look for all the record which have similar filter (which is a waste of time)
    # instead we use first() 
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not found")

    # print(post)
    return post
  
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    # To delete a record from a table
    # Filter out the data/ record and use delete() function (delete(synchronize_session=False) recommended) on the post
    # At last db.commit() will make changes to database  
    # for more refer document

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def Update_posts(id: int, post: Schemas.PostCreate, db: Session = Depends(get_db)):
    # To update a record from a table
    # Filter out the data/ record and use update() function (synchronize_session=False) recommended) on the post
    # At last db.commit() will make changes to database  
    # for more refer document

    Update_post = db.query(models.Post).filter(models.Post.id == id)

    if Update_post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} nto found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    Update_post.update(post.dict(),synchronize_session = False)
    db.commit()
    return Update_post.first()