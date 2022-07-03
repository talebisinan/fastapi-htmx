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


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    session_key = request.cookies.get("session_key", uuid.uuid4().hex)
    organizations = get_organizations(db, session_key)
    context = {
        "request": request,
        "organizations": organizations,
        "title": "Home",
        "orgs_count": len(organizations),
    }
    response = templates.TemplateResponse("home.html", context)
    response.set_cookie(key="session_key", value=session_key, expires=259200)  # 3 days
    return response


@app.post("/add", response_class=HTMLResponse)
async def post_add(
    request: Request, title: str = Form(...), db: Session = Depends(get_db)
):
    session_key = request.cookies.get("session_key")
    organization = create_organization(db, title=title, session_key=session_key)
    context = {"request": request, "organization": organization}
    await ws_manager.broadcast({"payload": {"count": get_organizations_count(db)}})
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
async def delete(item_id: int, db: Session = Depends(get_db)):
    delete_organization(db, item_id)
    await ws_manager.broadcast({"payload": {"count": get_organizations_count(db)}})


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
