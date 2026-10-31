from fastapi import FastAPI, HTTPException, status

from models.db import db
from models.models import Sheep

app = FastAPI()


@app.get("/sheep/", response_model=list[Sheep])
def read_all_sheep():
    return db.get_all_sheep()


@app.get("/sheep/{id}", response_model=Sheep)
def read_sheep(id: int):
    sheep = db.get_sheep(id)
    if sheep is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sheep not found")
    return sheep


@app.post("/sheep/", response_model=Sheep, status_code=status.HTTP_201_CREATED)
def add_sheep(sheep: Sheep):
    # Check if the sheep ID already exists to avoid duplicates
    if sheep.id in db.data:
        raise HTTPException(status_code=400, detail="Sheep with this ID already exists")

    # Add the new sheep to the database
    db.data[sheep.id] = sheep
    return sheep  # Return the newly added sheep data


@app.put("/sheep/{id}", response_model=Sheep)
def update_sheep(id: int, sheep: Sheep):
    try:
        return db.update_sheep(id, sheep)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sheep not found")


@app.delete("/sheep/{id}", response_model=Sheep)
def delete_sheep(id: int):
    try:
        return db.delete_sheep(id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sheep not found")
