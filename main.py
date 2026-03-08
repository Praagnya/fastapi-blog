from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id":1,
        "author": "Pragnya Narasimha",
        "title": "Transformers",
        "content": "Attention mechanism is so cool",
        "date_posted": "April 20, 2025"
    },
    {
        "id": 2,
        "author": "John Doe",
        "title": "Introduction to FastAPI",
        "content": "FastAPI is a modern web framework for building APIs",
        "date_posted": "March 15, 2025"
    },
    {
        "id": 3,
        "author": "Jane Smith",
        "title": "Python Best Practices",
        "content": "Writing clean and maintainable Python code",
        "date_posted": "February 10, 2025"
    }
]

@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"})

@app.get("/api/posts") 
def get_posts():
    return {"posts": posts}

@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return {"post": post}
    return {"error": "Post not found"}
    