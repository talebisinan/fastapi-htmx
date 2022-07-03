import uuid

from fastapi import Depends, WebSocket, WebSocketDisconnect
from fastapi import FastAPI, Form
from fastapi import Request, Response
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from models.organization import (
    create_organization,
    get_organizations,
    get_organization,
    get_organizations_count,
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


@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    session_key = request.cookies.get("session_key", uuid.uuid4().hex)
    return get_organizations(db, session_key)

@app.post("/add")
async def post_add(
    request: Request, title: str = Form(...), db: Session = Depends(get_db)
):
    session_key = request.cookies.get("session_key")
    return create_organization(db, title=title, session_key=session_key)

@app.get("/edit/{item_id}")
def get_edit(request: Request, item_id: int, db: Session = Depends(get_db)):
   return get_organization(db, item_id)


@app.put("/edit/{item_id}")
def put_edit(
    request: Request,
    item_id: int,
    title: str = Form(...),
    db: Session = Depends(get_db),
):
    return update_organization(db, item_id, title)


@app.delete("/delete/{item_id}")
async def delete(request: Request, item_id: int, db: Session = Depends(get_db)):
    session_key = request.cookies.get("session_key")
    return delete_organization(db, item_id)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, payload: dict):
        for connection in self.active_connections:
            await connection.send_json(payload)


ws_manager = ConnectionManager()


@app.websocket("/count")
async def count_of_orgs(websocket: WebSocket):
    await ws_manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
