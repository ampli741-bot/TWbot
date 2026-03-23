from aiogram import Router, types
import aiosqlite
import time
from db import DB_NAME

router = Router()

@router.message(lambda msg: msg.text == "📊 Статистика")
async def stats(msg: types.Message):
    now = int(time.time())
    today = now - 86400

    async with aiosqlite.connect(DB_NAME) as db:

        # 👥 всего
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        total = (await cursor.fetchone())[0]

        # 🔥 активные сегодня
        cursor = await db.execute(
            "SELECT COUNT(*) FROM users WHERE last_seen > ?",
            (today,)
        )
        active = (await cursor.fetchone())[0]

        # 🆕 новые сегодня (по id примерно)
        cursor = await db.execute(
            "SELECT COUNT(*) FROM users WHERE last_seen > ? AND last_farm = 0",
            (today,)
        )
        new_users = (await cursor.fetchone())[0]

    await msg.answer(
        f"📊 Статистика:\n\n"
        f"👥 Всего игроков: {total}\n"
        f"🔥 Активных сегодня: {active}\n"
        f"🆕 Новых сегодня: {new_users}"
    )