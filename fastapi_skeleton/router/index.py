import asyncio

from fastapi import APIRouter, WebSocket, Request
from starlette.templating import Jinja2Templates

from fastapi_skeleton.config.config import Config

router = APIRouter()

templates = Jinja2Templates(directory=Config.HTML_DIR)


async def log_reader(log_file_name: str, n=5):
    log_lines = ""
    with open(f"{Config.BASE_DIR}/{log_file_name}", "r", encoding="utf-8") as file:
        for line in file.readlines()[-n:]:
            if "ERROR" in line:
                log_lines += f'<p class="text-red-400">{line}</p><br/>'
            elif "WARNING" in line:
                log_lines += f'<p class="text-orange-300">{line}</p><br/>'
            else:
                log_lines += f"{line}<br/>"
        return log_lines


@router.websocket("/ws/log")
async def websocket_endpoint_log(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            await asyncio.sleep(0.1)
            logs = await log_reader("logs/info.log", 50)
            await websocket.send_text(logs)
    except Exception as e:
        print(e)
    finally:
        await websocket.close()


@router.get("/log")
async def get(request: Request):
    context = {
        "log_file": "info.log",
        "domain": request.client.host
    }
    return templates.TemplateResponse("log.html", {"request": request, "context": context})