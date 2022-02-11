from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import routes

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# route loader
for i in dir(routes):
    app.include_router(i.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
