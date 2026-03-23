from aiogram import Router, types
import aiosqlite
from db import DB_NAME, update_user

router = Router()

@router.message(lambda msg: msg.text == "🛡 Экипировать")
async def equip(msg: types.Message):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT name, power FROM items WHERE user_id = ? ORDER BY power DESC LIMIT 1",
            (msg.from_user.id,)
        )
        item = await cursor.fetchone()

    if not item:
        await msg.answer("❌ У тебя нет предметов")
        return

    name, power = item

    await update_user(msg.from_user.id, "equipped_power", power)

    await msg.answer(
        f"🛡 Экипировано:\n"
        f"{name} (+{power})\n\n"
        f"🔥 Теперь ты сильнее!"
    )