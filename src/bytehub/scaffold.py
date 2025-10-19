import shutil
from pathlib import Path
TEMPLATE_PATH = Path(__file__).parent / "templates" / "bot_template.py"

def scaffold(name: str, outdir: str = "."):
    out = Path(outdir) / name
    if out.exists():
        raise FileExistsError(str(out))
    out.mkdir(parents=True)
    shutil.copy(TEMPLATE_PATH, out / "bot.py")
    (out / "README.md").write_text(f"# {name}\nRun python bot.py after setting DISCORD_BOT_TOKEN")
    (out / ".gitignore").write_text(".env\nvenv/\n__pycache__/\n")
    return str(out.resolve())
