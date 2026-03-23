from aiogram import Router, types
import aiosqlite
from db import DB_NAME, get_user, update_user
from utils.loot import drop_loot

router = Router()

CASE_PRICE = 100

@router.message(lambda msg: msg.text == "🎰 Кейсы")
async def open_case(msg: types.Message):
    user = await get_user(msg.from_user.id)

    if not user:
        await msg.answer("❌ Напиши /start")
        return

    gold = int(user["gold"])  # ✅ фикс

    if gold < CASE_PRICE:
        await msg.answer("❌ Нужно 100 золота")
        return

    # 💸 списываем золото
    await update_user(msg.from_user.id, "gold", gold - CASE_PRICE)

    loot = drop_loot()

    if not loot:
        await msg.answer("😢 Кейс пустой...")
        return

    name, power = loot

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO items (user_id, name, power) VALUES (?, ?, ?)",
            (msg.from_user.id, name, power)
        )
        await db.commit()

    await msg.answer(f"🎰 Ты открыл кейс!\n🎁 {name} (+{power})")