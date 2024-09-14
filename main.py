from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/hotels")
def main():
    return ("Hello world!")

@app.put("/hotels/{hotel_id}")
def update_all(hotel_id: str):
    pass

@app.patch("/hotels/{hotel_id}")
def update_one(hotel_id: str):
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)