from fastapi import FastAPI
from app.routes import router
from app.database import init_db  

app = FastAPI(title="Admin API - Library Management")
app.include_router(router)

@app.on_event("startup")
def on_startup():
    init_db()  

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
