from fastapi import APIRouter
from starlette.responses import HTMLResponse

from app.controller.classification_controller import router as classification_router

all_routers = APIRouter()
all_routers.include_router(classification_router)


@all_routers.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <html>
        <head>
            <title>News Classifier</title>
        </head>
        <body>
            <h1>Welcome to News Classifier</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
