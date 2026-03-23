from aiogram import Router, types
import aiosqlite
from db import DB_NAME

router = Router()

@router.message(lambda msg: msg.text == "🎒 Инвентарь")
async def inventory(msg: types.Message):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT name, power FROM items WHERE user_id = ?",
            (msg.from_user.id,)
        )
        items = await cursor.fetchall()

    if not items:
        await msg.answer("🎒 Пусто")
        return

    text = "🎒 Твои предметы:\n\n"
    for item in items:
        text += f"{item[0]} (+{item[1]})\n"

    await msg.answer(text)