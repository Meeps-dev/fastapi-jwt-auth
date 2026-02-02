from fastapi import FastAPI
from app.database import Base, engine
from app.auth.routes import router as auth_router
from app.users.routes import router as users_router
from app.admin.routes import router as admin_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)


@app.get("/")
def root():
    return {"status": "JWT Auth System running"}
