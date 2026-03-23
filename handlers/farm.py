import time
import random
from aiogram import Router, types
from db import get_user, add_gold, update_user, DB_NAME
from utils.loot import drop_loot
import aiosqlite

router = Router()

@router.message(lambda msg: msg.text in ["/farm", "⛏️ Фарм"])
async def farm(msg: types.Message):
    user = await get_user(msg.from_user.id)

    if not user:
        await msg.answer("❌ Напиши /start")
        return

    now = int(time.time())
    last_farm = user["last_farm"]
    farm_level = user["farm_level"]

    # 🟢 первый запуск
    if last_farm == 0:
        await update_user(msg.from_user.id, "last_farm", now)
        await msg.answer("⛏️ Фарм начался... зайди позже")
        return

    elapsed = now - last_farm

    # максимум 3 часа
    elapsed = min(elapsed, 10800)

    if elapsed <= 0:
        await msg.answer("⏳ Подожди немного...")
        return

    # 💰 доход
    income = max(1, int(elapsed / 60 * farm_level * 20))

    await add_gold(msg.from_user.id, income)
    await update_user(msg.from_user.id, "last_farm", now)

    minutes = elapsed // 60

    await msg.answer(
        f"💰 Оффлайн фарм!\n"
        f"⏱ Ты был оффлайн: {minutes} мин\n"
        f"💵 Получено: {income} золота"
    )

    # ======================
    # 🎁 ЛУТ С ФАРМА
    # ======================

    # шанс 25%
    if random.random() < 0.25:
        loot = drop_loot()

        if loot:
            name, power = loot

            async with aiosqlite.connect(DB_NAME) as db:
                await db.execute(
                    "INSERT INTO items (user_id, name, power) VALUES (?, ?, ?)",
                    (msg.from_user.id, name, power)
                )
                await db.commit()

            await msg.answer(f"🎁 Ты нашёл предмет: {name} (+{power})")