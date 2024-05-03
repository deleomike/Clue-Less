from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi import (
    FastAPI,
)

from clueless import STATIC_PATH, TEMLPATES_PATH
from clueless.app.api import main_router
from clueless.app.ui.views import router as ui_router


app = FastAPI()

app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")
templates = Jinja2Templates(directory=TEMLPATES_PATH)

app.include_router(main_router, prefix="/api")
app.include_router(ui_router)

origins = ["http://localhost:8080",
           "https://localhost",
           "http://127.0.0.1:8080",
           "http://127.0.0.1",
           "http://127.0.0.1:80",
           "http://127.0.0.1:8000"
           "http://127.0.0.1:55102",
           "http://127.0.0.1:5500",
           "http://127.0.0.1:55100",
           "*",
           "https://container-service-1.vhkkrbli6vaf6.us-east-1.cs.amazonlightsail.com/",
           "http://127.0.0.1:55085"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    from clueless.app.db import create_db_and_tables, alchemy_create_db_and_tables
    create_db_and_tables()
    await alchemy_create_db_and_tables()



def start_app(port: int = 8080, host: str = "127.0.0.1", reload: bool = False):
    import uvicorn

    from clueless.settings import settings

    settings.BACKEND_HOST = host
    settings.BACKEND_PORT = port

    uvicorn.run(app="clueless.app.webapp:app", reload=reload, host=host, port=port, use_colors=True)


if __name__ == "__main__":

    start_app(port=8080, host="127.0.0.1", reload=True)

