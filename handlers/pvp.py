from aiogram import Router, types
import random
import aiosqlite
from db import get_user, update_user, add_gold, DB_NAME

router = Router()

@router.message(lambda msg: msg.text and "Атака" in msg.text)
async def pvp(msg: types.Message):
    user_id = msg.from_user.id

    user = await get_user(user_id)
    if not user:
        await msg.answer("❌ Напиши /start")
        return

    # 🔍 ищем другого игрока
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id != ? ORDER BY RANDOM() LIMIT 1",
            (user_id,)
        )
        target = await cursor.fetchone()

    if not target:
        await msg.answer("❌ Нет игроков для PvP")
        return

    target = dict(target)

    # ⚔️ атака
    player_attack = user.get("attack", 0) + user.get("equipped_power", 0)
    enemy_attack = target.get("attack", 0) + target.get("equipped_power", 0)

    player_damage = random.randint(max(1, player_attack - 2), player_attack + 2)
    enemy_damage = random.randint(max(1, enemy_attack - 2), enemy_attack + 2)

    # ❤️ HP
    player_hp = user.get("hp_current", 100)
    enemy_hp = target.get("hp_current", 100)

    enemy_hp -= player_damage
    player_hp -= enemy_damage

    # 🏆 победитель
    if player_hp > enemy_hp:
        reward = random.randint(10, 30)

        await add_gold(user_id, reward)
        await update_user(user_id, "pvp_wins", user.get("pvp_wins", 0) + 1)

        result_text = (
            f"⚔️ Ты победил игрока!\n"
            f"💥 Ты нанес: {player_damage}\n"
            f"❤️ Твоё HP: {max(player_hp, 0)}\n"
            f"💰 +{reward} золота"
        )
    else:
        loss = random.randint(5, 15)

        await add_gold(user_id, -loss)

        result_text = (
            f"💀 Ты проиграл!\n"
            f"💥 Враг нанес: {enemy_damage}\n"
            f"❤️ Твоё HP: {max(player_hp, 0)}\n"
            f"💸 -{loss} золота"
        )

    # 💾 сохраняем HP
    await update_user(user_id, "hp_current", max(player_hp, 0))

    await msg.answer(result_text)
