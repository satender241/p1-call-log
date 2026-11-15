"""
P1 call-log API: the KITCHEN of the restaurant.

It has two doors:
    GET  /calls  ->  read every call from the database (the pantry)
    POST /calls  ->  save one new call into the database

Run it on your laptop with:
    uvicorn main:app --reload
"""

import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from psycopg.rows import dict_row
from pydantic import BaseModel, Field

# --- Secrets ------------------------------------------------------------------
# On your laptop the database address comes from the .env file.
# On Render it comes from the "Environment" settings page. Never from this code.
load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

# --- The app ------------------------------------------------------------------
app = FastAPI(title="P1 call log")

# CORS: a browser only lets a page on one address (your Vercel page) read from
# another address (this API on Render) if the API says that's OK. This says OK.
# FRONTEND_URL can be "*" (anyone) or your Vercel link (only your page).
allowed_sites = os.environ.get("FRONTEND_URL", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[site.strip() for site in allowed_sites],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def open_pantry():
    """Open a connection to the Postgres database.
    dict_row means each row comes back like {"caller": "Asha", ...}, which turns into JSON easily."""
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


# When the server starts, make sure the "calls" table exists (safe to run every time).
with open_pantry() as conn:
    conn.execute((Path(__file__).parent / "schema.sql").read_text())


# --- What a new call must look like ----------------------------------------------
# This is the "is it valid?" check from the slides. If a request is missing
# caller or summary, FastAPI refuses it with a 4xx error before our code runs.
class NewCall(BaseModel):
    caller: str = Field(min_length=1, max_length=100)
    summary: str = Field(min_length=1, max_length=1000)


# --- The doors ------------------------------------------------------------------
@app.get("/")
def home():
    """A tiny 'I'm alive' door, handy for checking the server is awake."""
    return {"status": "ok", "try": "/calls"}


@app.get("/calls")
def list_calls():
    """GET /calls -> SELECT: read every call, newest first. Replies 200 OK + a JSON list."""
    with open_pantry() as conn:
        return conn.execute(
            "SELECT id, caller, summary, created_at FROM calls ORDER BY id DESC"
        ).fetchall()


@app.post("/calls", status_code=201)
def add_call(call: NewCall):
    """POST /calls -> INSERT: save one new call. Replies 201 Created + the saved call with its new id.

    The %s marks are placeholders: Postgres fills them in safely, so nobody can sneak
    extra SQL commands in through the caller or summary text (that attack is called SQL injection).
    """
    with open_pantry() as conn:
        return conn.execute(
            "INSERT INTO calls (caller, summary) VALUES (%s, %s) "
            "RETURNING id, caller, summary, created_at",
            (call.caller, call.summary),
        ).fetchone()
