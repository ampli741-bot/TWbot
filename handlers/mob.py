import time
import random
from aiogram import Router, types
from db import get_user, add_gold, update_user, DB_NAME
from utils.loot import drop_loot
import aiosqlite

router = Router()

MOBS = [
    ("🐀 Крыса", 5, 20),
    ("🐺 Волк", 10, 40),
    ("🧟 Зомби", 15, 60),
    ("👹 Орк", 25, 100),
    ("🐉 Дракон", 50, 300)
]

@router.message(lambda msg: msg.text == "👹 Моб")
async def fight_mob(msg: types.Message):
    user = await get_user(msg.from_user.id)

    if not user:
        await msg.answer("❌ Напиши /start")
        return

    now = int(time.time())

    # ======================
    # ⚡ ЭНЕРГИЯ (10 в час)
    # ======================
    energy = int(user["energy"])
    max_energy = int(user["max_energy"])
    last_energy_update = int(user["last_energy_update"])

    # 1 энергия = 360 сек (6 минут)
    regen = (now - last_energy_update) // 360

    if regen > 0:
        energy = min(max_energy, energy + regen)
        last_energy_update = now

        await update_user(msg.from_user.id, "energy", energy)
        await update_user(msg.from_user.id, "last_energy_update", last_energy_update)

    if energy <= 0:
        # показать таймер до следующей энергии
        next_energy = 360 - (now - last_energy_update) % 360
        minutes = next_energy // 60
        seconds = next_energy % 60

        await msg.answer(f"⚡ Нет энергии!\n⏳ +1 через {minutes}м {seconds}с")
        return

    # списываем энергию
    await update_user(msg.from_user.id, "energy", energy - 1)

    # ======================
    # ⏳ КУЛДАУН БОЯ
    # ======================
    last_fight = int(user["last_fight"])

    if now - last_fight < 10:
        await msg.answer("⏳ Подожди перед следующим боем...")
        return

    await update_user(msg.from_user.id, "last_fight", now)

    # ======================
    # ❤️ HP
    # ======================
    max_hp = int(user["hp"])
    hp = int(user["hp_current"])
    last_hp_update = int(user["last_hp_update"])

    regen_hp = (now - last_hp_update) // 60

    if regen_hp > 0:
        hp = min(max_hp, hp + regen_hp)
        await update_user(msg.from_user.id, "hp_current", hp)
        await update_user(msg.from_user.id, "last_hp_update", now)

    if hp <= 0:
        await msg.answer("💀 У тебя нет HP! Подожди восстановления")
        return

    # ======================
    # ⚔️ БОЙ
    # ======================
    base_attack = int(user["attack"])
    bonus = int(user["equipped_power"])
    total_attack = base_attack + bonus

    name, mob_hp, reward = random.choice(MOBS)

    player_power = random.randint(total_attack // 2, total_attack)

    # ======================
    # ✅ ПОБЕДА
    # ======================
    if player_power >= mob_hp:
        await add_gold(msg.from_user.id, reward)
        await update_user(msg.from_user.id, "mob_wins", int(user["mob_wins"]) + 1)

        xp_gain = reward // 2
        level = int(user["level"])
        xp = int(user["xp"])

        new_xp = xp + xp_gain
        need_xp = level * 100

        text = f"⚔️ Ты победил {name}!\n💰 +{reward}\n⭐ +{xp_gain} XP"

        if new_xp >= need_xp:
            level += 1
            new_xp = 0

            new_attack = base_attack + 2

            await update_user(msg.from_user.id, "level", level)
            await update_user(msg.from_user.id, "attack", new_attack)

            text += f"\n🎉 Уровень {level}!"

        else:
            await update_user(msg.from_user.id, "xp", new_xp)

        loot = drop_loot()
        if loot:
            item_name, power = loot

            async with aiosqlite.connect(DB_NAME) as db:
                await db.execute(
                    "INSERT INTO items (user_id, name, power) VALUES (?, ?, ?)",
                    (msg.from_user.id, item_name, power)
                )
                await db.commit()

            text += f"\n🎁 {item_name} (+{power})"

        await msg.answer(text)

    # ======================
    # ❌ ПОРАЖЕНИЕ
    # ======================
    else:
        gold = int(user["gold"])
        hp = int(user["hp_current"])

        penalty_gold = max(5, int(gold * 0.1))
        penalty_hp = 20

        await update_user(msg.from_user.id, "gold", max(0, gold - penalty_gold))
        await update_user(msg.from_user.id, "hp_current", max(0, hp - penalty_hp))

        await msg.answer(
            f"💀 Ты проиграл {name}\n"
            f"💸 -{penalty_gold} золота\n"
            f"❤️ -{penalty_hp} HP"
        )