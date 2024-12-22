from fastapi import FastAPI,Request,WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils import htmx_templates
from pydantic import BaseModel
import json
from bar_utils.locate import locatePerc
import numpy as np
from bar_utils.map import mapping
from bar_utils.conversion import convert

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

class bar:
    def __init__(self,websocket:WebSocket,id:str):
        self.id = id
        self.socket:WebSocket = websocket
        self.progress:int = 0
        self.text:str = ""
        self.bar_task:asyncio.Task = None

        self.pause_event = asyncio.Event()
        self.pause_event.set()

    async def barTask(self,speed,interval):
        print("barTask started",speed,interval)
        speed,interval = int(speed),int(interval)
        intervals = 100/speed
        print("intervals")
       
        for i in range(int(intervals)):
            await self.pause_event.wait()
            self.progress += speed
            
            message = {
                "event":"progress",
                "id":self.id,
                "text":await locatePerc(self.progress/100),
                "time":mapping(convert(self.progress/100))[0],
                "progress":self.progress,
                "interval": interval
            }
            print(message)
            
            await self.socket.send_json(message)
            await asyncio.sleep(interval)

    async def pauseBar(self):
        self.pause_event.clear()

    async def continueBar(self):
        self.pause_event.set()

    async def start(self,settings):
        print("starting",settings)
        if self.bar_task == None:
            print("new task")
            self.bar_task = asyncio.create_task(self.barTask(settings["speed"],settings["interval"]))
        else:
            await self.continueBar()

        



class bar_client:
    def __init__(self,websocket:WebSocket):
        self.websocket:WebSocket = websocket
        self.bars:np.ndarray = np.array([],dtype=object)
    
    async def connect_bar(self,id):
     
        self.bars = np.append(self.bars,bar(self.websocket,id))

    async def get_bar(self,id) -> bar:
        for index,bar in enumerate(self.bars):
            if bar.id == id:
                return bar
    
        
    async def start_bar(self,id,settings):
        br = await self.get_bar(id)
        await br.start(settings)

    async def pause_bar(self,id):
        br = await self.get_bar(id)
        await br.pauseBar()


    
            
            
    

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
        print("invalid format",data)
        return 
    print(msg_json)
    if event == "start":
        client:bar_client = await manager.get_client(websocket)
        settings = {
            "speed":msg_json.get("speed",5),
            "interval":msg_json.get("interval",1)
        }
        await client.start_bar(msg_json.get("id"),settings)

    if event == "connect_bar":
        client:bar_client = await manager.get_client(websocket)
        await client.connect_bar(msg_json.get("id"))

    if event == "pause":
        print("pausing")
        client:bar_client  = await manager.get_client(websocket)
        await client.pause_bar(msg_json.get("id"))

manager = con_manager()

@app.websocket("/bar")
async def barHandle(websocket:WebSocket):
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