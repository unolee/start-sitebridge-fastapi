from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from datetime import datetime
import sqlite3
import os

app = FastAPI()

# CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:5173", "http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
DB_DIR = Path(os.environ.get("DB_DIR", str(Path(__file__).resolve().parent.parent / "data")))
DB_PATH = DB_DIR / "app.db"


def get_db():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS welcome (
            id INTEGER PRIMARY KEY,
            message TEXT NOT NULL
        )
    """)
    # Seed default welcome message
    row = db.execute("SELECT COUNT(*) FROM welcome").fetchone()
    if row[0] == 0:
        db.execute(
            "INSERT INTO welcome (id, message) VALUES (1, ?)",
            ("Welcome to SiteBridge! 🚀 Your FastAPI + React app is up and running.",),
        )
    db.commit()
    db.close()


init_db()


# API routes
@app.get("/api/hello")
async def hello():
    db = get_db()
    row = db.execute("SELECT message FROM welcome WHERE id = 1").fetchone()
    db.close()
    message = row["message"] if row else "Hello from SiteBridge!"
    return {"message": message, "timestamp": datetime.now().isoformat()}


@app.get("/api/items")
async def list_items():
    db = get_db()
    items = [dict(row) for row in db.execute("SELECT * FROM items ORDER BY id DESC").fetchall()]
    db.close()
    return items


@app.post("/api/items")
async def create_item(data: dict):
    db = get_db()
    db.execute("INSERT INTO items (title) VALUES (?)", (data.get("title", "Untitled"),))
    db.commit()
    db.close()
    return {"ok": True}


# Static files (SPA)
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


@app.get("/")
async def root():
    index = STATIC_DIR / "index.html"
    if index.exists():
        return FileResponse(index)
    return {"message": "API Server (FastAPI) - Client not built"}


if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
