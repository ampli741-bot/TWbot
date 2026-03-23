import time
from aiogram import Router, types
from db import get_user, update_user, add_gold

router = Router()

@router.message(lambda msg: msg.text == "🎁 Награда")
async def daily(msg: types.Message):
    user = await get_user(msg.from_user.id)

    now = int(time.time())
    last = user[11]  # last_daily

    if now - last < 86400:
        await msg.answer("⏳ Уже забрал сегодня!")
        return

    reward = 200

    await add_gold(msg.from_user.id, reward)
    await update_user(msg.from_user.id, "last_daily", now)

    await msg.answer(f"🎁 Ты получил {reward} золота!")