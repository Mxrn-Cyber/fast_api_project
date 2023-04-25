from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine
from core.setting import setting

from modules.user.controller import router as user_router
from modules.user.seed import user_seed

is_dev = setting.NAME == 'Development'
app = FastAPI() if is_dev else FastAPI(docs_url=is_dev, redoc_url=is_dev)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    # user_seed()


@app.on_event("shutdown")
def shutdown():
    engine.dispose()


@app.get('/')
def welcome():
    return f'Welcome to API'
