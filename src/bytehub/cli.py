import typer, os, secrets, subprocess
from typing import Optional
from .scaffold import scaffold
from .manager import BotInstance

app = typer.Typer()

def prompt_env(var: str, hide: bool = False):
    val = typer.prompt(var, default="")
    if not val and var == "SESSION_SECRET":
        val = secrets.token_urlsafe(32)
        typer.echo(f"generated SESSION_SECRET")
    return val

@app.command()
def setup(auto_run: bool = False):
    typer.echo("ByteBub setup")
    admin = prompt_env("ADMIN_API_KEY")
    client_id = prompt_env("MANAGED_BOT_CLIENT_ID")
    client_secret = prompt_env("MANAGED_BOT_CLIENT_SECRET")
    managed_token = prompt_env("MANAGED_BOT_TOKEN")
    session = prompt_env("SESSION_SECRET")
    with open(".env", "w") as f:
        f.write(f"ADMIN_API_KEY={admin}\n")
        f.write(f"MANAGED_BOT_CLIENT_ID={client_id}\n")
        f.write(f"MANAGED_BOT_CLIENT_SECRET={client_secret}\n")
        f.write(f"MANAGED_BOT_TOKEN={managed_token}\n")
        f.write(f"SESSION_SECRET={session}\n")
    typer.echo("wrote .env")
    if auto_run:
        try:
            subprocess.run(["docker","build",".","-t","ghcr.io/bytehub/bytebub-discord-multitool:latest"], check=True)
            subprocess.run(["docker","run","-d","-p","8000:8000","--env-file",".env","ghcr.io/bytehub/bytebub-discord-multitool:latest"], check=True)
            typer.echo("docker started")
        except Exception as e:
            typer.echo(f"docker failed: {e}")

def app_entry():
    app()

if __name__ == "__main__":
    app()
