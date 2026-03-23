from aiogram import Router, types
import aiosqlite
from db import DB_NAME

router = Router()

@router.message(lambda msg: msg.text == "🏆 Топ")
async def top(msg: types.Message):

    async with aiosqlite.connect(DB_NAME) as db:

        # 💰 ТОП ЗОЛОТО
        gold = await db.execute(
            "SELECT username, gold FROM users ORDER BY gold DESC LIMIT 5"
        )
        gold = await gold.fetchall()

        # 👹 ТОП МОБЫ
        mobs = await db.execute(
            "SELECT username, mob_wins FROM users ORDER BY mob_wins DESC LIMIT 5"
        )
        mobs = await mobs.fetchall()

        # ⚔️ ТОП PvP
        pvp = await db.execute(
            "SELECT username, pvp_wins FROM users ORDER BY pvp_wins DESC LIMIT 5"
        )
        pvp = await pvp.fetchall()

        # 💪 ТОП СИЛА
        power = await db.execute(
            "SELECT username, attack + equipped_power FROM users ORDER BY (attack + equipped_power) DESC LIMIT 5"
        )
        power = await power.fetchall()

    text = "🏆 ТОП ИГРОКОВ\n\n"

    # 💰 ЗОЛОТО
    text += "💰 Золото:\n"
    for i, row in enumerate(gold, 1):
        name = row[0] or "Игрок"
        text += f"{i}. {name} — {row[1]}\n"

    # 👹 МОБЫ
    text += "\n👹 Мобы:\n"
    for i, row in enumerate(mobs, 1):
        name = row[0] or "Игрок"
        text += f"{i}. {name} — {row[1]}\n"

    # ⚔️ PvP
    text += "\n⚔️ PvP:\n"
    for i, row in enumerate(pvp, 1):
        name = row[0] or "Игрок"
        text += f"{i}. {name} — {row[1]}\n"

    # 💪 СИЛА
    text += "\n💪 Сила:\n"
    for i, row in enumerate(power, 1):
        name = row[0] or "Игрок"
        text += f"{i}. {name} — {row[1]}\n"

    await msg.answer(text)