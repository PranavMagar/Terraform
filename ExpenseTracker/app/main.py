from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
from app.database import engine, Base
from app.routers import auth, expenses, reports

import time
from sqlalchemy.exc import OperationalError

# Create tables with retry
max_retries = 5
retry_interval = 2

for i in range(max_retries):
    try:
        Base.metadata.create_all(bind=engine)
        break
    except OperationalError as e:
        if i == max_retries - 1:
            raise e
        print(f"Database not ready, retrying in {retry_interval}s...")
        time.sleep(retry_interval)

app = FastAPI(title=settings.PROJECT_NAME)

# Middleware
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Routers
app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(reports.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
