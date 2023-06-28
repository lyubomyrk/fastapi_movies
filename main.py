import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date


class Movie(BaseModel):
    name: str
    release: date
    directors: str
    gross: float


database = {
    1: Movie(name="Avatar", release=date(2009, 12, 16), directors="James Cameron", gross=785_221_649),
    2: Movie(name="Avengers: Endgame", release=date(2019, 4, 26), directors="Anthony Russo, Joe Russo", gross=858_373_000),
    3: Movie(name="Star Wars: Episode VII - The Force Awakens", release=date(2015, 12, 18), directors="J.J. Abrams", gross=936_662_225)
}


app = FastAPI()


@app.get("/")
async def root():
    return {"greeting": "Welcome to the awesome movie database!"}


@app.get("/movies/{movie_id}")
async def get_movie_by_id(movie_id: int):
    if database.get(movie_id):
        return database[movie_id]
    else:
        return {"error": "can't find the movie with id given!"}


@app.post("/movies/")
async def add_movie_by_id(movie_id: int, movie: Movie):
    if existing_movie := database.get(movie_id):
        return existing_movie
    else:
        database.update({movie_id: movie})
        return movie.dict()


@app.put("/movies/")
async def update_movie_by_id(movie_id: int, movie: Movie):
    if database.get(movie_id):
        database[movie_id] = movie
        return movie.dict()
    else:
        return {"error": "this movie_id doesn't exist!"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
