from datetime import datetime
import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

app = FastAPI(title="Wedding Invitation")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # позже можно ограничить своим доменом
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")


class Confirmation(BaseModel):
    family: str
    guests: dict[str, bool]


@app.post("/confirm")
def confirm(data: Confirmation):

    lines = []

    for guest, present in data.guests.items():
        icon = "✅" if present else "❌"
        lines.append(f"{icon} {guest}")

    message = (
        "💍 Новое подтверждение присутствия\n\n"
        f"👨‍👩‍👧 Семья: {data.family}\n\n"
        + "\n".join(lines)
        + f"\n\n🕒 {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=10,
    )

    if response.status_code != 200:
        return {
            "success": False,
            "telegram": response.text
        }

    return {
        "success": True
    }
