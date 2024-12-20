from fastapi import FastAPI,Request,WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils import htmx_templates
from pydantic import BaseModel
import json
import numpy as np

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

class bar_client:
    def __init__(self,websocket:WebSocket):
        self.websocket:WebSocket = websocket
        self.progress:int = 0
        self.text:str = ""

        self.bar_task = None

    async def start(self):
        for i in range(10):
            self.progress += 10
            print("progress")
            await self.websocket.send_text(htmxTemplates.render(filename="partials/bar.jinja",mappings={"progress":self.progress}))
            await asyncio.sleep(1)
            
            
    

class con_manager:
    def __init__(self):
        self.connections:np.ndarray = np.array([],dtype=bar_client)
    
    async def connect(self,websocket:WebSocket):
        try:
            await websocket.accept()
            self.connections = np.append(self.connections,bar_client(websocket))
           
            
           
        except Exception as e:
            print(e)

    async def disconnect(self,websocket):
        for index,client in enumerate(self.connections):
            if client.websocket == websocket:
                np.delete(self.connections,index)
                break

    async def get_client(self,websocket:WebSocket):
      
        for index,client in enumerate(self.connections):
           
            if client.websocket == websocket:
                return client
   

async def handleMessage(websocket:WebSocket,data:str):
    try:
        msg_json:dict = json.loads(data)
        event:str = msg_json.get("event")
    except:
        print("invalid format")
        return 
    
    if event == "start":
        client:bar_client = await manager.get_client(websocket)
        await client.start()
        print("start")
        
        




manager = con_manager()

@app.websocket("/bar")
async def bar(websocket:WebSocket):
    await manager.connect(websocket)
    
    while True:
        try:
            data = await websocket.receive_text()
            await handleMessage(websocket,data)
        except WebSocketDisconnect:
            await manager.disconnect(websocket)
            break


@app.get("/sample")
async def sample(request:Request):
    print("sample req")
    return templates.TemplateResponse("/partials/sample.html",{"request":request})

@app.get("/")
async def index(request:Request):
    return templates.TemplateResponse("index.html",{"request":request,"progress":0})

@app.get("/barTemp")
async def temp(request: Request):
    return templates.TemplateResponse("/partials/bar.jinja", {"request": request,"progress":"10"})



if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app="server:app",reload=True,port=8000)