# frontend_api/app/main.py

from fastapi import FastAPI
from app.routes import router
from app.database import init_db
from app.messaging import start_background_subscriber

app = FastAPI(title="Frontend API - Library Catalogue")
app.include_router(router)

@app.on_event("startup")
def on_startup():
    init_db()  
    start_background_subscriber()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
