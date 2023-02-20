from typing import Union
from routers import players, teams, seasons, statlines, games
from db.database import create_db_and_tables
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
app.include_router(games.router)
app.include_router(seasons.router)
app.include_router(statlines.router)

# === Stat Endpoints ===
# """ 
# Want to follow the syntax of /{entity}/{entity.id}/stats
# That way we can get the data of an individual player, team, game, season but for the entity
# For example /players/2/stats will return all the statlines for the player with the matching ID
# Can let the front end handle the aggregation and math. That should hopefully reduce the need for any 
# preprocessing or query strings in the URL.
# """