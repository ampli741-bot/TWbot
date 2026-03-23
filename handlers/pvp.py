from aiogram import Router, types
import random
import aiosqlite
from db import get_user, update_user, add_gold, DB_NAME

router = Router()

@router.message(lambda msg: "Атака" in msg.text)
async def pvp(msg: types.Message):
    user_id = msg.from_user.id
    user = await get_user(user_id)

    if not user:
        await msg.answer("❌ Напиши /start")
        return

    # 🔍 ищем случайного игрока
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id != ? ORDER BY RANDOM() LIMIT 1",
            (user_id,)
        )
        target = await cursor.fetchone()

    if not target:
        await msg.answer("❌ Нет игроков для PvP")
        return

    # 🧠 преобразуем в dict
    target = dict(target)

    # ⚔️ расчёт урона
    player_attack = user["attack"] + user["equipped_power"]
    enemy_attack = target["attack"] + target["equipped_power"]

    player_damage = random.randint(player_attack - 2, player_attack + 2)
    enemy_damage = random.randint(enemy_attack - 2, enemy_attack + 2)

    # ❤️ HP
    player_hp = user["hp_current"]
    enemy_hp = target["hp_current"]

    enemy_hp -= player_damage
    player_hp -= enemy_damage

    # 🧾 результат боя
    if player_hp > enemy_hp:
        winner = "player"
    else:
        winner = "enemy"

    # 💰 награда / штраф
    if winner == "player":
        reward = random.randint(10, 30)
        await add_gold(user_id, reward)
        await update_user(user_id, "pvp_wins", user["pvp_wins"] + 1)

        text = (
            f"⚔️ Ты победил!\n"
            f"💥 Урон: {player_damage}\n"
            f"❤️ Осталось HP: {player_hp}\n"
            f"💰 Получено: {reward} золота"
        )
    else:
        loss = random.randint(5, 15)
        await add_gold(user_id, -loss)

        text = (
            f"💀 Ты проиграл!\n"
            f"💥 Враг ударил: {enemy_damage}\n"
            f"❤️ Осталось HP: {player_hp}\n"
            f"💸 Потеряно: {loss} золота"
        )

    # 💾 сохраняем HP
    await update_user(user_id, "hp_current", max(player_hp, 0))

    await msg.answer(text)
