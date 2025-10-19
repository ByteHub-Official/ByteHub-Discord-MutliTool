import os, subprocess, venv, psutil
from pathlib import Path

class BotInstance:
    def __init__(self, path: str, env: dict = None):
        self.path = Path(path)
        self.env = dict(os.environ)
        if env:
            self.env.update(env)
        self.proc = None
        self.venv_dir = self.path / "venv"

    def ensure_venv(self):
        if not self.venv_dir.exists():
            venv.create(self.venv_dir, with_pip=True)
        pip = self.venv_dir / "bin" / "pip"
        req = self.path / "requirements.txt"
        if req.exists():
            subprocess.check_call([str(pip), "install", "-r", str(req)], env=self.env)

    def start(self, entry="bot.py"):
        python = self.venv_dir / "bin" / "python"
        self.proc = subprocess.Popen([str(python), str(self.path / entry)], env=self.env)
        return self.proc.pid

    def is_running(self):
        return self.proc and psutil.pid_exists(self.proc.pid)

    def stop(self):
        if self.proc and psutil.pid_exists(self.proc.pid):
            psutil.Process(self.proc.pid).terminate()
            return True
        return False
