import asyncio
import atexit
import json
import dotenv
import os
from anthropic import AsyncAnthropic

dotenv.load_dotenv(".env")


api = os.getenv("ANTHROPIC")

client = AsyncAnthropic(
    api_key=api
)
model_name = "claude-3-5-haiku-20241022"

with open('system.txt', "r") as f:
    sys = f.read()


async def gen_cont(msg):

    message = await client.messages.create(
        model=model_name,
        max_tokens=512,
        system=sys,
        messages=[{"role": "user", "content": msg}],
        temperature=0.9
    )
    return message.content[0].text


try:
    with open('mappings.json', 'r') as f:
        mappings = json.load(f)
except Exception:
    mappings = {}


async def gen(msg, val):
  
    if mappings.get(str(val)):
       return
  
    try:
        out = await gen_cont(msg)
        mappings[val] = out
    except:
       out = ""

    while True:
        try:
            out = await gen_cont(msg)
            mappings[val] = out
            print("passed",msg,out)
            break
        except Exception as e:
          
           print("retrying",msg)
           await asyncio.sleep(30)

async def mass(msgList):
   print("running mass")
   tasks = [gen(msg[0],msg[1]) for msg in msgList]
   await asyncio.gather(*tasks)


def log_map():
    with open('mappings.json', 'w') as f:
        json.dump(mappings, f,indent=4)

