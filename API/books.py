from fastapi import FastAPI,Body

app = FastAPI()

Books = [
    {'Title' : 'Title One', 'Author' : 'Auther One', 'Group' : 'Science'},
    {'Title' : 'Title Two', 'Author' : 'Auther Two', 'Group' : 'Science'},
    {'Title' : 'Title Three', 'Author' : 'Auther Three', 'Group' : 'math'},
    {'Title' : 'Title Four', 'Author' : 'Auther Four', 'Group' : 'math'},
    {'Title' : 'Title Five', 'Author' : 'Auther Five', 'Group' : 'Science'}
]

@app.get("/apiendpoint")
async def first_apiendpoint():
    return {'message' : 'Hello World!'}

@app.get("/books")
async def get_books():
    return Books

@app.get("/books/my_books")
async def print_dynamic_para():
    return {'message' : 'myfavbooks'}

@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in Books:
        if book.get('Title').casefold() == book_title.casefold():
            return book
    return "None"

@app.get("/books/")
async def read_category(group: str):
    books_toreturn = []
    for book in Books:
        if book.get('Group').casefold() == group.casefold():
            books_toreturn.append(book)
    return books_toreturn

@app.post("/books/create_book")
async def create_books(new_book = Body()):
    Books.append(new_book)

@app.put("/books/update_book")
async def update_books(updated_book = Body()):
    for i in range(len(Books)):
        if Books[i].get('Title').casefold() == updated_book.get('Title').casefold():
            Books[i] = updated_book







