# FastAPI Blog

A simple blog application built with FastAPI and Jinja2 templates.

## Features

- Server-side rendered pages with Jinja2 templates
- REST API endpoints for posts
- Bootstrap 5 UI with dark/light mode toggle
- Static file serving for CSS and images

## Requirements

- Python 3.12+

## Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

## Running the App

```bash
fastapi dev main.py
```

The app will be available at http://127.0.0.1:8000

## Endpoints

| Route | Description |
|-------|-------------|
| `/` | Home page with blog posts |
| `/posts` | Same as home page |
| `/api/posts` | JSON API returning all posts |

## Project Structure

```
.
├── main.py              # FastAPI application
├── pyproject.toml       # Project configuration
├── static/              # Static assets (CSS, images, icons)
└── templates/           # Jinja2 templates
    ├── layout.html      # Base template
    └── home.html        # Home page template
```
