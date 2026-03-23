from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Профиль")],
            [KeyboardButton(text="⛏️ Фарм"), KeyboardButton(text="⬆️ Улучшить")],
            [KeyboardButton(text="⚔️ Атака")],
            [KeyboardButton(text="🎒 Инвентарь")],
            [KeyboardButton(text="🛡 Экипировать")],
            [KeyboardButton(text="👹 Моб")],
            [KeyboardButton(text="🎰 Кейсы")],
            [KeyboardButton(text="🏆 Топ")],
            [KeyboardButton(text="⚒ Перековать")],
            [KeyboardButton(text="📊 Статистика")]
        ],
        resize_keyboard=True
    )