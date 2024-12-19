from fastapi import FastAPI,Request,WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils import htmx_templates
from pydantic import BaseModel

import asyncio

app = FastAPI()

templates = Jinja2Templates(directory="templates")
htmxTemplates = htmx_templates("templates")
app.mount("/static",StaticFiles(directory="static"),name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


class bar_res(BaseModel):
    progress: int
    time: int
    text: str

class con_manager:
    def __init__(self):
        self.connections = []
    
    async def connect(self,websocket:WebSocket):
        try:
            await websocket.accept()
            self.connections.append(websocket)
            await websocket.send_text(htmxTemplates.render("partials/sample.html",{"content":"hi"}))
        except Exception as e:
            print(e)

    async def disconnect(self,websocket):
        self.connections.remove(websocket)


manager = con_manager()

@app.websocket("/bar")
async def bar(websocket:WebSocket):
    await manager.connect(websocket)
    
    while True:
        try:
            data = await websocket.receive_text()
            print(data)
        except WebSocketDisconnect:
            await manager.disconnect(websocket)
            break


@app.get("/sample")
async def sample(request:Request):
    print("sample req")
    return templates.TemplateResponse("/partials/sample.html",{"request":request})

@app.get("/")
async def index(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})

@app.get("/barTemp")
async def temp(request: Request):
    return templates.TemplateResponse("/partials/bar.html", {"request": request,"progress":"10"})



if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app="server:app",reload=True,port=8000)