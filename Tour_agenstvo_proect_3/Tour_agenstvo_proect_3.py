from fastapi import *
import time



app = FastAPI()


@app.get("/health", status_code=200)
def health():
    return {"status": "ok"}
