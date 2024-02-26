import time
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    Contents: str
    published: bool = True
    rating: Optional[float] = None

while True:
    try:
        conn = psycopg2.connect(host = 'localhost',database = 'FastAPI',user = 'postgres',password = 'Aptean@123', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("Database connected successfully")
        break
    except Exception as error:
        print("Not connect to database")
        print("error : ",error)
        time.sleep(2)

my_posts = [{"title": "My fav places", "Contents": "Hawaii", "id": 1}, {
        "title": "my fav food", "Contents": "Dosa", "id": 2}]


def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post


def find_index(id):
    for ind, post in enumerate(my_posts):
        if post['id'] == id:
            return ind


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():

    cursor.execute(""" SELECT * FROM fastapi """)
    posts = cursor.fetchall()
    # print(posts) 
    return {"data": posts}


# @app.post("/posts")
# def create_posts(payload: dict = Body(...)):
#     print(payload['title'])
#     return {"message": f"title: {payload['title']} contents: {payload['Contents']}"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def dynamic_post(new_post: Post):

    # post_dict = new_post.dict()
    # post_dict['id'] = randrange(1, 100000)
    # my_posts.append(post_dict)

    cursor.execute(""" INSERT INTO fastapi (title,"Content") VALUES (%s,%s) RETURNING * """, (new_post.title,new_post.Contents,))
    my_post = cursor.fetchone()
    # conn.commit()
    print(my_post)
    return {"data": my_post}

@app.post("/posts/{id}", status_code=status.HTTP_201_CREATED)
def dynamic_post(id : int, new_post: Post):

    # post_dict = new_post.dict()
    # post_dict['id'] = randrange(1, 100000)
    # my_posts.append(post_dict)

    cursor.execute(""" INSERT INTO fastapi (title,"Content",id) VALUES (%s,%s,%s) RETURNING * """, (new_post.title,new_post.Contents,str(id),))
    my_post = cursor.fetchone()
    # conn.commit()
    print(my_post)
    return {"data": my_post}


@app.get("/posts/{id}")
def find_posts(id: int, response: Response):

    cursor.execute(""" SELECT * FROM fastapi WHERE id =%s""",str(id))
    my_post = cursor.fetchone()
    # post = find_post(id)
    if not my_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not found")
    return {"details": my_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):

    cursor.execute(""" DELETE FROM fastapi WHERE id = %s""", (str(id),))
    test_post = cursor.fetchone()
    conn.commit()

    # index = find_index(id)
    if test_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def Update_posts(id: int, post: Post):

    cursor.execute(""" UPDATE fastapi SET title=%s, "Content"=%s WHERE id=%s RETURNING *""",(post.title,post.Contents,str(id),))
    testpost = cursor.fetchone()
    print(testpost)

    if testpost == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} nto found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    return {"data": testpost}
