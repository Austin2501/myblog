from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
from datetime import datetime
from fastapi.responses import RedirectResponse

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route to show all posts
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY created_at DESC').fetchall()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts})

# Route to create a new post
@app.get("/create", response_class=HTMLResponse)
async def create_get(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.post("/create")
async def create_post(title: str = Form(...), content: str = Form(...)):
    conn = get_db_connection()
    conn.execute('INSERT INTO posts (title, content, created_at) VALUES (?, ?, ?)',
                 (title, content, datetime.now()))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=302)

# Route to delete a post
@app.delete("/delete/{id}")
async def delete_post(id: int):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return JSONResponse(content={"message": "Post deleted successfully!"}, status_code=200)

# Route to edit a post
@app.get("/edit/{id}", response_class=HTMLResponse)
async def edit_get(id: int, request: Request):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    conn.close()
    return templates.TemplateResponse("edit.html", {"request": request, "post": post})

@app.post("/edit/{id}")
async def edit_post(id: int, title: str = Form(...), content: str = Form(...)):
    conn = get_db_connection()
    conn.execute('UPDATE posts SET title = ?, content = ?, created_at = ? WHERE id = ?',
                 (title, content, datetime.now(), id))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=302)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
