import random
from aiogram import Router, types
from db import get_user, add_gold, update_user

router = Router()

@router.message(lambda msg: msg.text == "⚔️ Атака")
async def info(msg: types.Message):
    await msg.answer("Ответь на сообщение игрока с этой кнопкой")

@router.message(lambda msg: msg.reply_to_message)
async def attack(msg: types.Message):
    attacker_id = msg.from_user.id
    target_id = msg.reply_to_message.from_user.id

    attacker = await get_user(attacker_id)
    target = await get_user(target_id)

    if not target:
        await msg.answer("Игрок не найден")
        return

    # ⚔️ атака
    base_attack = attacker[2]
    bonus = attacker["equipped_power"]  # ⚠️ правильный индекс
    total_attack = base_attack + bonus

    damage = random.randint(total_attack // 2, total_attack)

    # ✅ ПОБЕДА
    if damage > target[3] // 2:
        reward = 20
        await add_gold(attacker_id, reward)

        # 🏆 счётчик PvP
        await update_user(attacker_id, "pvp_wins", attacker[13] + 1)

        await msg.answer(f"⚔️ Победа! +{reward} золота")

    # ❌ ПОРАЖЕНИЕ
    else:
        await msg.answer("❌ Поражение")