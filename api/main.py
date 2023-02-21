from typing import Union
from db.models import *
from db.database import engine, create_db_and_tables
from sqlmodel import Session, select
from dependencies import get_session
from routers import players, teams, seasons, games, statlines
from fastapi import FastAPI, HTTPException, Depends



app = FastAPI()

# === Startup Function ===
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
# === API Information ===
@app.get("/")
def root():
    return {
        "Version": "0.0.1",
        "Author":"@naterobertstech",
        "LastUpdated": "2023-02-16"
        }

app.include_router(players.router)
app.include_router(teams.router)
app.include_router(seasons.router)
app.include_router(games.router)
app.include_router(statlines.router)

