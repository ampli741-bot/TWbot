from aiogram import Router, types
from db import get_user, update_user

router = Router()

@router.message(lambda msg: msg.text == "⬆️ Улучшить")
async def upgrade(msg: types.Message):
    user = await get_user(msg.from_user.id)

    if not user:
        await msg.answer("❌ Напиши /start")
        return

    gold = user["gold"]
    farm_level = user["farm_level"]

    cost = farm_level * 50

    if gold < cost:
        await msg.answer(f"❌ Нужно {cost} золота")
        return

    await update_user(msg.from_user.id, "gold", gold - cost)
    await update_user(msg.from_user.id, "farm_level", farm_level + 1)

    await msg.answer(f"🚀 Фарм улучшен до {farm_level + 1} уровня!")