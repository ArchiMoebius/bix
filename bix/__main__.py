from contextlib import asynccontextmanager
from pathlib import PosixPath

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from rich.traceback import install

from bix.api import book, category, linkcategorybook, linkreaderbook, reader
from bix.database import create_db_and_tables

install(show_locals=True)


def cli():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        create_db_and_tables()
        yield

    app = FastAPI(lifespan=lifespan)

    app.include_router(book.router)
    app.include_router(reader.router)
    app.include_router(category.router)
    app.include_router(linkreaderbook.router)
    app.include_router(linkcategorybook.router)

    templates = Jinja2Templates(
        directory=PosixPath(__file__).parent.joinpath("templates")
    )

    @app.get("/", response_class=RedirectResponse, status_code=302)
    async def _():
        return "/books.html"

    @app.get("/books.html")
    async def _(request: Request, response_class=HTMLResponse):
        return templates.TemplateResponse("/pages/books.html", {"request": request})

    @app.get("/readers.html")
    async def _(request: Request, response_class=HTMLResponse):
        return templates.TemplateResponse("/pages/readers.html", {"request": request})

    @app.get("/categories.html")
    async def _(request: Request, response_class=HTMLResponse):
        return templates.TemplateResponse(
            "/pages/categories.html", {"request": request}
        )

    @app.get("/add_book.html")
    async def _(request: Request, response_class=HTMLResponse):
        return templates.TemplateResponse("/pages/add_book.html", {"request": request})

    @app.get("/add_reader.html")
    async def _(request: Request, response_class=HTMLResponse):
        return templates.TemplateResponse(
            "/pages/add_reader.html", {"request": request}
        )

    @app.get("/add_category.html")
    async def _(request: Request, response_class=HTMLResponse):
        return templates.TemplateResponse(
            "/pages/add_category.html", {"request": request}
        )

    @app.get("/reader_books.html")
    async def _(request: Request, response_class=HTMLResponse):
        return templates.TemplateResponse(
            "/pages/reader_books.html", {"request": request}
        )

    @app.get("/category_books.html")
    async def _(request: Request, response_class=HTMLResponse):
        return templates.TemplateResponse(
            "/pages/category_books.html", {"request": request}
        )

    @app.get("/reader.html")
    async def _(request: Request, response_class=HTMLResponse):
        return templates.TemplateResponse("/pages/reader.html", {"request": request})

    @app.get("/book.html")
    async def _(request: Request, response_class=HTMLResponse):
        return templates.TemplateResponse("/pages/book.html", {"request": request})

    @app.get("/category.html")
    async def _(request: Request, response_class=HTMLResponse):
        return templates.TemplateResponse("/pages/category.html", {"request": request})

    app.mount(
        "/",
        StaticFiles(directory=PosixPath(__file__).parent.joinpath("static")),
        name="static",
    )

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    cli()
