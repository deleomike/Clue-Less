from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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


@app.on_event("startup")
async def on_startup():
    from clueless.app.db import create_db_and_tables, alchemy_create_db_and_tables
    create_db_and_tables()
    await alchemy_create_db_and_tables()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="webapp:app", reload=True, host="127.0.0.1", port=8000)