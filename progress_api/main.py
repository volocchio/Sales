"""SMARTWING Sales Training – Progress Tracking API.

Stores per-user section completion status and notes in SQLite.
"""

from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Generator

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Sales Training Progress API")

DB_PATH = os.environ.get("DB_PATH", "/data/progress.db")


# ── database ────────────────────────────────────────────────────────
@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    with get_db() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT    UNIQUE NOT NULL,
                role       TEXT    DEFAULT 'rep',
                created_at TEXT    DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS progress (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL,
                section_id TEXT    NOT NULL,
                completed  INTEGER DEFAULT 0,
                notes      TEXT    DEFAULT '',
                updated_at TEXT    DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(user_id, section_id)
            )"""
        )
        conn.commit()


init_db()


# ── models ──────────────────────────────────────────────────────────
class UserCreate(BaseModel):
    name: str


class ProgressUpdate(BaseModel):
    section_id: str
    completed: bool = False
    notes: str = ""


class BulkProgress(BaseModel):
    items: list[ProgressUpdate]


# ── endpoints ───────────────────────────────────────────────────────
@app.get("/api/users")
def list_users():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT id, name, role, created_at FROM users ORDER BY name"
        ).fetchall()
        return [dict(r) for r in rows]


@app.post("/api/users")
def create_or_get_user(user: UserCreate):
    name = user.name.strip()
    if not name:
        raise HTTPException(400, "Name required")
    with get_db() as conn:
        existing = conn.execute(
            "SELECT id, name, role FROM users WHERE LOWER(name) = LOWER(?)", (name,)
        ).fetchone()
        if existing:
            return dict(existing)
        conn.execute("INSERT INTO users (name) VALUES (?)", (name,))
        conn.commit()
        new = conn.execute(
            "SELECT id, name, role FROM users WHERE LOWER(name) = LOWER(?)", (name,)
        ).fetchone()
        return dict(new)


@app.get("/api/progress/{user_id}")
def get_progress(user_id: int):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT section_id, completed, notes, updated_at "
            "FROM progress WHERE user_id = ?",
            (user_id,),
        ).fetchall()
        return {
            r["section_id"]: {
                "completed": bool(r["completed"]),
                "notes": r["notes"],
                "updated_at": r["updated_at"],
            }
            for r in rows
        }


@app.post("/api/progress/{user_id}")
def save_progress(user_id: int, update: ProgressUpdate):
    now = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        conn.execute(
            """INSERT INTO progress (user_id, section_id, completed, notes, updated_at)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(user_id, section_id) DO UPDATE SET
                   completed  = excluded.completed,
                   notes      = excluded.notes,
                   updated_at = excluded.updated_at""",
            (user_id, update.section_id, int(update.completed), update.notes, now),
        )
        conn.commit()
    return {"ok": True}


@app.post("/api/progress/{user_id}/bulk")
def save_bulk(user_id: int, bulk: BulkProgress):
    now = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        for item in bulk.items:
            conn.execute(
                """INSERT INTO progress (user_id, section_id, completed, notes, updated_at)
                   VALUES (?, ?, ?, ?, ?)
                   ON CONFLICT(user_id, section_id) DO UPDATE SET
                       completed  = excluded.completed,
                       notes      = excluded.notes,
                       updated_at = excluded.updated_at""",
                (user_id, item.section_id, int(item.completed), item.notes, now),
            )
        conn.commit()
    return {"ok": True, "saved": len(bulk.items)}


@app.get("/api/dashboard")
def dashboard():
    with get_db() as conn:
        users = conn.execute(
            "SELECT id, name, role, created_at FROM users ORDER BY name"
        ).fetchall()
        result = []
        for u in users:
            rows = conn.execute(
                "SELECT section_id, completed, notes, updated_at "
                "FROM progress WHERE user_id = ? ORDER BY updated_at DESC",
                (u["id"],),
            ).fetchall()
            completed = sum(1 for r in rows if r["completed"])
            last_active = rows[0]["updated_at"] if rows else None
            sections = {
                r["section_id"]: {
                    "completed": bool(r["completed"]),
                    "notes": r["notes"],
                    "updated_at": r["updated_at"],
                }
                for r in rows
            }
            result.append(
                {
                    "id": u["id"],
                    "name": u["name"],
                    "role": u["role"],
                    "created_at": u["created_at"],
                    "completed_count": completed,
                    "last_active": last_active,
                    "sections": sections,
                }
            )
        return result
