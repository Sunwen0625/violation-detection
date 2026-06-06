from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import test_db_connection
from app.core.database import Base, engine


from app.api.user_api import router as user_router
from app.api.police_api import router as police_router
from app.api.report_api import router as report_router
from app.api.car_api import router as car_router
from app.api.violation_api import router as violation_router
from app.api.appeal_api import router as appeal_router


app = FastAPI()
origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API running"}


@app.get("/db-check")
def db_check():
    return {"database": test_db_connection()}

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(police_router)
app.include_router(report_router)
app.include_router(car_router)
app.include_router(violation_router)
app.include_router(appeal_router)
