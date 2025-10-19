import os
from fastapi import FastAPI, HTTPException, Header, Depends, Request
from pydantic import BaseModel
from pathlib import Path
from typing import Optional
from ..scaffold import scaffold
from ..manager import BotInstance
import secrets, httpx

app = FastAPI(title="ByteBub Discord MultiTool")
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")
MANAGED_CLIENT_ID = os.getenv("MANAGED_BOT_CLIENT_ID")
MANAGED_CLIENT_SECRET = os.getenv("MANAGED_BOT_CLIENT_SECRET")
SESSION_SECRET = os.getenv("SESSION_SECRET") or secrets.token_urlsafe(32)

def require_admin(x_api_key: Optional[str] = Header(None)):
    if not ADMIN_API_KEY or x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="unauthorized")

class CreateBotRequest(BaseModel):
    name: str

@app.post("/create-bot", dependencies=[Depends(require_admin)])
def create_bot(req: CreateBotRequest):
    base = Path.cwd() / "bots"
    base.mkdir(exist_ok=True)
    path = scaffold(req.name, outdir=str(base))
    return {"status": "created", "path": path}

@app.get("/status/{path:path}", dependencies=[Depends(require_admin)])
def status(path: str):
    inst = BotInstance(path)
    return {"path": path, "running": inst.is_running()}

@app.get("/auth/install-managed-bot")
def install_managed_bot():
    if not MANAGED_CLIENT_ID:
        raise HTTPException(status_code=400, detail="client id not set")
    url = f"https://discord.com/oauth2/authorize?client_id={MANAGED_CLIENT_ID}&scope=bot%20applications.commands&permissions=0"
    return {"url": url}

@app.get("/auth/oauth-callback")
async def oauth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="no code")
    token_url = "https://discord.com/api/oauth2/token"
    data = {
        "client_id": MANAGED_CLIENT_ID,
        "client_secret": MANAGED_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": str(request.url_for("oauth_callback")),
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    async with httpx.AsyncClient() as client:
        r = await client.post(token_url, data=data, headers=headers)
    if r.status_code != 200:
        raise HTTPException(status_code=400, detail="token exchange failed")
    return r.json()
