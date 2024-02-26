from typing import Optional
from fastapi import FastAPI  ### Importing FastAPI from fastapi library
from fastapi.params import Body ### Body parameter isa pydantic model used to get data from the user's input
from pydantic import BaseModel ### Importing pydantic model
from random import randrange  ### To provide randome integer in bteween some specified range
from fastapi import Response,status ### To validate the response to send it to front end of the user and status of the query
from fastapi import HTTPException ### To raise http exceptions while performing any path operations
import psycopg2 ### To Connect to postgres instance
from psycopg2.extras import RealDictCursor ### This is to retrive the values with column names in dictionary format
import time ### To use time functions


app = FastAPI()

### To work with postgres SQL module required ---> psycopg
# To install Psycopg2 cmd --> pip install psycopg2
# Psycopg Reference --> https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries


# Making an connection to postgres existing database
# Here we are using try-except function to find a prefect connection and use of while loop helps to try connecting to database until a connection is found
# This while loop keeps asking contantly for the connection there should be some leverage time to sync up with database ( for ex : issue with internet) 
while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'FastAPI', user = 'postgres', password = 'Aptean@123', cursor_factory= RealDictCursor)  # The 'conn' is the variable used to connect database
        cursor = conn.cursor()  # Cursor is the varaible used to do functions on the database using api calls (acts as pointor)
        print('Database Connection Successful!!')
        break
    except Exception as error:
        print('Not connected')
        time.sleep(2)  # To set timer for 2 seconds

# Github page for refrence --> https://github.com/Sanjeev-Thiyagarajan/fastapi-course

# Pydantic Model -> this defines the schema for the data input
# Whenever an user provides the data different from the data type provided to each specific variable or missing out required field to will automatically throws an error (Con)
# More about pydatic models -> https://docs.pydantic.dev/latest/usage/models/
# Opitonal keyword is to make a datatype optional

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# Temporary List to store posts/ articles
my_posts = [{"title" : "New Title","content":"new content","id":1} , {"title" : "New Title1","content":"new content1","id":2}]

# More about http methods ->  https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods

# This get method to get data 
# This works on priority of fist come first serve

# @app.get("/")
# def create_post():
#     return {"message" : "this is a created post"}

@app.get("/")
def root():
    return {"message": "Hello World!!"}


# When list is the output of the get function automatically gets converted to json format (Using FastAPI)
# @app.get("/posts") 
# def get_posts():
#     return {"data": my_posts}

# When there is get function for a database
# fetchall --> this function gets all the records in the database
# fetchmany --> this function takes an argument on how many records needs to returned from the database
# fetchone --> this function gets single record when there is only one possiblity of returning a record
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""") # Execute cmd is used to make sql cmds on the database 
    posts = cursor.fetchall() # fetching the details according to the execute command
    # print(posts)
    return {"data" : posts}


# This post method to create a new data
# This can cause database failure if the client/user is not providing data in proper format
# To avoid this conflict or overcome this issue 
# we make use of pydatic model

# Here data schema is title: str, content: str
# @app.post("/")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"data": f"title : {payload['title']} contents : {payload['content']}"}

# This is a post method with a proper schema data (Pydantic model) 
# We use .dict() to convert the pydantic output to dictionary/json format

# CRUD - Create, Read, Update and Delete --> these are 4 main functions to create a application.
# If no error or the data is published then webclient returns 200 http status code
# But for creating or delete or not found etc for those kind of status needs to specified which is not 
# So we provide the status code for it in path operator if the particular path is succefully published

# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(payload: Post):
#     # print(payload)
#     post_dict = payload.dict()
#     post_dict['id'] = randrange(0,10000000)
#     my_posts.append(post_dict)
#     return {"data": post_dict}


#SQL Injection error ---> SQL injection is a code injection technique used to attack data-driven applications, in which malicious SQL statements are inserted into an entry field for execution.
# This function is using api call db
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(payload: Post):
    # cursor.execute(f"INSERT INTO posts(title,content,published) VALUES ({payload.title},{payload.content},{payload.published})")   This not used because of SQL injection error
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""", (payload.title,payload.content,payload.published))
    post = cursor.fetchone()
    conn.commit() # This commit function saves the data in the database which api is connected to
    # print(post)
    return {"data": post}


# Retriving a single post from the data
# Here {id} represent the path parameter
# @app.get("/posts/{id}")
# def get_post(id: int, response: Response):
#     # print(type(id))
#     post = find_post(id)
#     if not post:
#         response.status_code = status.HTTP_404_NOT_FOUND  # This line is to confirm there aren't any posts with given specfic id and we are 404 not found error status to users
#         return {"message" : f"The post with given {id} was not found...."}
#     return {"message" :  post}


# Instead sending hardcoded error message we use httpexceptions to send or raise exceptions
# In the above code 'response' is taken as parameter to set hardcoded status code if an error is raised
# @app.get("/posts/{id}")
# def get_post(id: int):
#     # print(type(id))
#     post = find_post(id)
#     if not post:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
#                              detail=f"The post with given {id} was not found....")
#     return {"message" :  post}

# This function is to get particular record from db
@app.get("/posts/{id}")
def get_post(id: int):
    # print(type(id))
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(str(id)))  # Here returning * is not required because it already returning some value as we are using select 
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                             detail=f"The post with given {id} was not found....")
    return {"message" :  post}



# when this below function is executed or published and tried to execute path with get function it throws an error
# This reason for the error is due to the above function where the {id} is considered an variable so in place of variable, We also know that the function which comes first gets executed first
# So in /posts/latest path "latest" is considered an variable which is same as id whihc expects integer but provided with string error
# To overcome this error we need to order the requests or change the url(path parameters )
 
# @app.get_latest("/posts/latest")
# def get_latest_posts():
#     post = my_posts[len(my_posts)-1]
#     return {"data": post}


# Function to find the specific post using id provided by the user
def find_post(id):
    for post in my_posts:
        print(type(post['id']))
        if post['id'] == id:
            return post
    return None




# deleting a post from a list
# Here we are searching for the id's index which needs to deleted
# The default status code for delete is 204 http status code
# Since we are setting default status code as 204 which is no content so it throws an error when we snd a message
# So instead of sending message or json output send status response

# @app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):

#     index = find_index(id)
#     if not index:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail= f"Index not found for id = {id}")
#     my_posts.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


#This function is to delete a record from the daabase
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Index not found for id = {id}")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Function to find the specific index
def find_index(id):
    for i,post in enumerate(my_posts):
        if post['id'] == id:
            return i
    return None


# Updating a post
# There are 2 ways of updating post using put and patch method
# Put Method -->  it requires all the required fields to update a post
# Patch Method --> it requires only the field which need to updated with primary key to identify the post

# Put Method
# @app.put("/posts/{id}")
# def Update_post(id: int, payload: Post):

#     index = find_index(id)
#     if not index:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail= f"Index not found for id = {id}")
    
#     post = payload.dict()
#     post['id'] = id
#     my_posts[index] = post

#     return {"Data" : post}

# Updating a record in the database
@app.put("/posts/{id}")
def Update_post(id: int, payload: Post):

    cursor.execute("""UPDATE posts SET title =%s,content =%s,published = %s  WHERE id = %s RETURNING *""",(payload.title,payload.content,payload.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Index not found for id = {id}")

    return {"Data" : updated_post}

### Automatically fastapi provides the documentations
### The simple way to get the documentation page is to add /docs at the end of path


# Patch Method
# @app.patch("/posts/{id}")
# def Update_postsRating(id: int, payload: dict = Body(...)):

#     index = find_index(id)
#     if not index:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail= f"Index not found for id = {id}")
    
#     post = payload.dict()
#     post['id'] = id

#     return {"Data" : my_posts[index]['title']}


