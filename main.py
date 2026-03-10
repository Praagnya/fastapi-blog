from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

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

@app.get("/posts/{post_id}", include_in_schema=False)
def post_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            title = post["title"][:50] + "..." if len(post["title"]) > 50 else post["title"]
            return templates.TemplateResponse(request, "post.html", {"post": post, "title": title})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.get("/api/posts") 
def get_posts():
    return {"posts": posts}

@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return {"post": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An unexpected error occurred. Please try again later."
    )

    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request, 
        "error.html",
        {
            "status_code": exception.status_code,
            "message": message,
            "title": f"{exception.status_code} Error"
        },
        status_code=exception.status_code
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "Invalid request data. Please check your input and try again.",
            "title": "422 Error"
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )

