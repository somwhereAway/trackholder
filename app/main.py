import os
import asyncio
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from telegram import Update

import tg_bot.tgbot_core as tgbot_core
app = FastAPI(docs_url=None, redoc_url=None)

templates = Jinja2Templates(directory="templates")

requests_list = []


@app.post("/telegram/")
async def handle_webhook(request: Request):
    data = await request.json()  # Получаем данные в формате JSON
    requests_list.append(data)  # Сохраняем запрос в список
    await tgbot_core.tgbot.ptb_app.update_queue.put(
        Update.de_json(
            data=data, bot=tgbot_core.tgbot.ptb_app.bot
        )
    )
    return {"status": "ok"}

templates = Jinja2Templates(directory=os.path.join(
    os.path.dirname(__file__), '.', 'templates'))


@app.get("/", response_class=HTMLResponse)
async def get_requests(request: Request):
    return templates.TemplateResponse(
        "index.html",
        # {"request": request, "requests": requests_list}
    )


async def main():
    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=app,
            port=8000,
            use_colors=True,
            host='0.0.0.0',
        )
    )
    async with tgbot_core.tgbot.ptb_app:
        await tgbot_core.tgbot.ptb_app.start()
        await webserver.serve()
        await tgbot_core.tgbot.ptb_app.stop()


if __name__ == '__main__':
    asyncio.run(main())
