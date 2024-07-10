from typing import Optional
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from __init__ import environment
from endpoint_function import ping,set_group_ips,get_blacklists,get_ips,stop_demon,start_demon,restart_demon,status_demon,get_review_blacklists
from database import create_table_bloqueos

if (environment == 'production'):
    create_table_bloqueos()
    app = FastAPI()
else:
    create_table_bloqueos()
    app = FastAPI(debug=True)

# ----- CLASES MODELOS DE DATOS -----

class ips_groups(BaseModel):
    ranges: str
    ips: str

# ----- ENDPOINTS -----

@app.get("/",status_code=200)
def status():
    return ping()

@app.post("/protected/set_group_ips/",status_code=200)
def set_group_ip(ips_group:ips_groups):
    return set_group_ips(ips_group)

@app.get("/get_blacklist",status_code=200)
async def get_blacklist():
    return get_blacklists()

@app.get("/get_ip/{ip}",status_code=200)
async def get_ip(ip):
    return get_ips(ip)

@app.get("/start_review/",status_code=200)
async def start_review():
    return start_demon()

@app.get("/stop_review/",status_code=200)
async def stop_review():
    return stop_demon()

@app.get("/restart_review/",status_code=200)
async def restart_review():
    return restart_demon()

@app.get("/status_review/",status_code=200)
async def status_review():
    return status_demon()
"""
@app.get("/get_review_blacklist",status_code=200)
async def get_review_blacklist():
    return get_review_blacklists()
"""

if __name__ == "__main__":
    if (environment == 'production'):
        uvicorn.run(app, host="0.0.0.0", port=8080)
    else:
        uvicorn.run(app, host="0.0.0.0", port=8080,debug=True)
