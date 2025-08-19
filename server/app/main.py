from fastapi import FastAPI
import uvicorn


app = FastAPI()

@app.get("/")
async def index():
    return {"status":"ok"}


if __name__ == "__main__":
    uvicorn.run(app=app)
