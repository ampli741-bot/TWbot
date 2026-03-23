from aiogram import Router, types
import aiosqlite
from db import DB_NAME

router = Router()

@router.message(lambda msg: msg.text == "⚒ Перековать")
async def craft(msg: types.Message):
    user_id = msg.from_user.id

    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT name, COUNT(*), power FROM items WHERE user_id = ? GROUP BY name",
            (user_id,)
        )
        items = await cursor.fetchall()

        for item in items:
            name = item[0]
            count = item[1]
            power = item[2]

            if count >= 3:
                # 🗑 удаляем 3 предмета
                await db.execute(
                    "DELETE FROM items WHERE id IN (SELECT id FROM items WHERE user_id = ? AND name = ? LIMIT 3)",
                    (user_id, name)
                )

                # ➕ создаём улучшенный
                new_power = power + 2

                await db.execute(
                    "INSERT INTO items (user_id, name, power) VALUES (?, ?, ?)",
                    (user_id, name, new_power)
                )

                await db.commit()

                await msg.answer(f"⚒ Перековка!\n{name} улучшен до +{new_power}")
                return

    await msg.answer("❌ Нет предметов для перековки (нужно 3 одинаковых)")