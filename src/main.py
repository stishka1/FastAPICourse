import uvicorn
from fastapi import FastAPI

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent)) # для папки src, далее уже идет роутинг с src

from src.api.hotels import router as router_hotels


app = FastAPI()

app.include_router(router_hotels)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)