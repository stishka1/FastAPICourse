from fastapi import FastAPI, Body
import uvicorn

app = FastAPI()

hotels = [
    {
        "id": 1,
        "name": "Resort&SPA",
        "title": "Turkish"
    },
    {
        "id": 2,
        "name": "Miami Beach",
        "title": "Indonesia"
    },
    {
        "id": 3,
        "name": "EcoLine Resort",
        "title": "Gvinea Hotel"
    }
]

@app.get("/")
def main():
    global hotels

    return hotels

@app.post("/hotels/{hotel_id}")
def add_hotel(hotel_id: int, title: str | None = Body(None), name: str | None = Body(None)):
    global hotels
    if hotel_id not in hotels:
        hotels.append(
                {
                    "id": hotel_id,
                    "name": name,
                    "title": title,
                }
            )
    return {"status": "200"}

@app.put("/hotels/{hotel_id}")
def update_all(hotel_id: int, title: str = Body(), name: str = Body()):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"]== hotel_id][0]
    hotel["name"] = name
    hotel["title"] = title

    return hotels

@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    for i in hotels:
        if hotel_id == i['id']:
            hotels.remove(i)
    return {"status": "200"}



@app.patch("/hotels/{hotel_id}")
def update_one(hotel_id: int, title: str | None = Body(None), name: str | None = Body(None)):

    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"]== hotel_id][0]


    if title:
        hotel["title"] = title
    if name:
        hotel["name"] = name

    return {"status": "200"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)