from aiogram import Router, types
from db import get_user

router = Router()

@router.message(lambda msg: msg.text in ["/profile", "👤 Профиль"])
async def profile(msg: types.Message):
    user = await get_user(msg.from_user.id)

    if not user:
        await msg.answer("❌ Напиши /start")
        return

    await msg.answer(
        f"👤 Герой:\n"
        f"🏆 Уровень: {user['level']}\n"
        f"⭐ XP: {user['xp']}/{user['level']*100}\n\n"
        f"💰 Золото: {user['gold']}\n"
        f"⚔️ База атака: {user['attack']}\n"
        f"🛡 Бонус: {user['equipped_power']}\n"
        f"🔥 Итог атака: {user['attack'] + user['equipped_power']}\n\n"
        f"❤️ HP: {user['hp_current']}/{user['hp']}\n"
        f"⛏️ Уровень фарма: {user['farm_level']}"
        f"⚡ Энергия: {user['energy']}/{user['max_energy']}\n"
    )