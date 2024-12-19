import json
import numpy as np
import asyncio
from conversion import convert


with open("mappings.json","r") as f:
    content = json.load(f)

keys = np.array([float(k) for k in content.keys()])

def closest(num):
    
    ind = (np.abs(keys-num)).argmin()
    return [content[str(keys[ind])],keys[ind]]

async def locate(num):
    num = float(num)
    cont,date = closest(num)
    return cont

async def locatePerc(num):
    return await locate(convert(num))
