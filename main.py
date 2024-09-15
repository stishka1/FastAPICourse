from fastapi import FastAPI, Body
import uvicorn

app = FastAPI()

global hotels

hotels = [
    {
        id: 1,
        "name": "Resort&SPA",
        "title": "Turkish"
    },
    {
        id: 2,
        "name": "Miami Beach",
        "title": "Indonesia"
    },
    {
        id: 3,
        "name": "EcoLine Resort",
        "title": "Gvinea Hotel"
    }
]

@app.get("/")
def main():
    return ("Hello world!")

@app.post("hotels")
def add_hotel(id: int, title: str = Body(), name: str = Body()):
    pass

@app.put("/hotels/{hotel_id}")
def update_all(hotel_id: str, title: Body(), name: Body()):
    global hotels
    # hotel = {k, v in hotels}

@app.patch("/hotels/{hotel_id}")
def update_one(hotel_id: str, title: Body(), name: Body()):
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)