import uuid
from datetime import timedelta

from fastapi import Depends
from fastapi import FastAPI, Form
from fastapi import Request

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

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def organizations(request: Request, db: Session = Depends(get_db)):
    session_key = request.cookies.get("session_key", uuid.uuid4().hex)
    return get_organizations(db, session_key)


@app.post("/add")
async def add_organization(
    request: Request, title: str = Form(...), db: Session = Depends(get_db)
):
    session_key = request.cookies.get("session_key")
    return create_organization(db, title=title, session_key=session_key)


@app.get("/edit/{item_id}")
async def get_organization_edit(
    request: Request, item_id: int, db: Session = Depends(get_db)
):
    return get_organization(db, item_id)


@app.put("/edit/{item_id}")
async def put_organization_edit(
    request: Request,
    item_id: int,
    title: str = Form(...),
    db: Session = Depends(get_db),
):
    return update_organization(db, item_id, title)


@app.delete("/delete/{item_id}")
async def delete_org(item_id: int, db: Session = Depends(get_db)):
    return delete_organization(db, item_id)
