import uuid
from datetime import timedelta

from fastapi import Depends
from fastapi import FastAPI, Form
from fastapi import Request, Response
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from models.organization import (
    create_organization,
    get_organizations,
    get_organization,
    update_organization,
    delete_organization,
)
from database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    session_key = request.cookies.get("session_key", uuid.uuid4().hex)
    organizations = get_organizations(db, session_key)
    context = {"request": request, "organizations": organizations, "title": "Home"}
    response = templates.TemplateResponse("home.html", context)
    response.set_cookie(key="session_key", value=session_key, expires=259200)  # 3 days
    return response


@app.post("/add", response_class=HTMLResponse)
def post_add(request: Request, title: str = Form(...), db: Session = Depends(get_db)):
    session_key = request.cookies.get("session_key")
    organization = create_organization(db, title=title, session_key=session_key)
    context = {"request": request, "organization": organization}
    return templates.TemplateResponse("organizations/item.html", context)


@app.get("/edit/{item_id}", response_class=HTMLResponse)
def get_edit(request: Request, item_id: int, db: Session = Depends(get_db)):
    organization = get_organization(db, item_id)
    context = {"request": request, "organization": organization}
    return templates.TemplateResponse("organizations/edit.html", context)


@app.put("/edit/{item_id}", response_class=HTMLResponse)
def put_edit(
    request: Request,
    item_id: int,
    title: str = Form(...),
    db: Session = Depends(get_db),
):
    organization = update_organization(db, item_id, title)
    context = {"request": request, "organization": organization}
    return templates.TemplateResponse("organizations/item.html", context)


@app.delete("/delete/{item_id}", response_class=Response)
def delete(item_id: int, db: Session = Depends(get_db)):
    delete_organization(db, item_id)
