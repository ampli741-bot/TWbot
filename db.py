import aiosqlite
import time

TEST_MODE = False

DB_NAME = "test.db" if TEST_MODE else "game.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:

        # =========================
        # 👤 USERS
        # =========================
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            gold INTEGER DEFAULT 100,
            attack INTEGER DEFAULT 5,
            hp INTEGER DEFAULT 100,
            hp_current INTEGER DEFAULT 100,
            last_hp_update INTEGER DEFAULT 0,
            farm_level INTEGER DEFAULT 1,
            last_farm INTEGER DEFAULT 0,
            equipped_power INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            xp INTEGER DEFAULT 0,
            last_daily INTEGER DEFAULT 0,
            last_fight INTEGER DEFAULT 0,
            mob_wins INTEGER DEFAULT 0,
            pvp_wins INTEGER DEFAULT 0
        )
        """)

        # =========================
        # 🎒 ITEMS
        # =========================
        await db.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            power INTEGER
        )
        """)

        # =========================
        # 🔥 МИГРАЦИИ
        # =========================

        try:
            await db.execute("ALTER TABLE users ADD COLUMN energy INTEGER DEFAULT 10")
        except:
            pass

        try:
            await db.execute("ALTER TABLE users ADD COLUMN max_energy INTEGER DEFAULT 10")
        except:
            pass

        try:
            await db.execute("ALTER TABLE users ADD COLUMN last_energy_update INTEGER DEFAULT 0")
        except:
            pass

        try:
            await db.execute("ALTER TABLE users ADD COLUMN last_seen INTEGER DEFAULT 0")
        except:
            pass

        try:
            await db.execute("ALTER TABLE users ADD COLUMN version INTEGER DEFAULT 1")
        except:
            pass

        await db.commit()


# =========================
# 👤 ПОЛЬЗОВАТЕЛЬ
# =========================

async def add_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, last_farm) VALUES (?, ?)",
            (user_id, 0)
        )
        await db.commit()


async def get_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )
        user = await cursor.fetchone()

        if user:
            return dict(user)
        return None


async def update_user(user_id, field, value):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            f"UPDATE users SET {field} = ? WHERE user_id = ?",
            (value, user_id)
        )
        await db.commit()


async def add_gold(user_id, amount):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE users SET gold = gold + ? WHERE user_id = ?",
            (amount, user_id)
        )
        await db.commit()