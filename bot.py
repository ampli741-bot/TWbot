import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from db import init_db
from handlers import mob
from handlers import top
from handlers import craft
from handlers import stats

from handlers import start, profile, farm, pvp, upgrade, inventory, equip, case

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    await init_db()

    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(farm.router)
    dp.include_router(pvp.router)
    dp.include_router(upgrade.router)
    dp.include_router(inventory.router)
    dp.include_router(equip.router)
    dp.include_router(case.router)
    dp.include_router(mob.router)
    dp.include_router(top.router)
    dp.include_router(craft.router)
    dp.include_router(stats.router)

    print("БОТ ЗАПУЩЕН")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())