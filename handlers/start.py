from aiogram import Router, types
from db import get_user, add_user, update_user
from utils.keyboard import main_menu
import time

router = Router()

@router.message(lambda msg: msg.text in ["/start", "старт"])
async def start(msg: types.Message):
    user = await get_user(msg.from_user.id)

    if not user:
        await add_user(msg.from_user.id)

    # 👤 имя
    username = msg.from_user.username or msg.from_user.first_name or "Игрок"
    await update_user(msg.from_user.id, "username", username)

    # 🔥 фикс активности
    await update_user(msg.from_user.id, "last_seen", int(time.time()))

    await msg.answer(
        "🍺 Добро пожаловать в Taverna War!",
        reply_markup=main_menu()
    )