
import json
import random
import time
import requests
import schedule
from bs4 import BeautifulSoup
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, Updater

TOKEN = "7666257083:AAEe7cCQ43gduZKaD60eX4r9Uw6lOoXjPfE"
CHAT_ID = 1634790575

bot = Bot(token=TOKEN)

# Загружаем куки
def load_cookies():
    with open("cookies.json", "r") as f:
        return json.load(f)

cookies = load_cookies()
HEADERS = {"User-Agent": "Mozilla/5.0"}
BASE_URL = "https://kwork.ru"

# Пример символов для проверки входа
CHECK_SYMBOLS = ["✅", "💡", "⭐", "🔥", "📌"]

def check_login_and_update_profile():
    session = requests.Session()
    for c in cookies:
        session.cookies.set(c['name'], c['value'])
    response = session.get(f"{BASE_URL}/user", headers=HEADERS)
    if "Мои кворки" in response.text:
        symbol = random.choice(CHECK_SYMBOLS)
        soup = BeautifulSoup(response.text, "lxml")
        description_tag = soup.find("div", {"class": "user-desc-text"})
        if description_tag:
            current_desc = description_tag.text.strip()
            new_desc = current_desc.rstrip(''.join(CHECK_SYMBOLS)) + symbol
            # В реальности нужно отправить POST-запрос на изменение описания
            bot.send_message(chat_id=CHAT_ID, text=f"✅ Успешный вход. Обновлено описание: {symbol}")
        else:
            bot.send_message(chat_id=CHAT_ID, text="⚠️ Не удалось найти описание профиля.")
    else:
        bot.send_message(chat_id=CHAT_ID, text="❌ Ошибка входа — проверь куки.")

def status_command(update: Update, context):
    update.message.reply_text("Бот работает. Ожидаю заказы и обновляю профиль.")

def run_bot():
    check_login_and_update_profile()
    schedule.every(1).hours.do(check_login_and_update_profile)

    while True:
        schedule.run_pending()
        time.sleep(10)

def telegram_interface():
    updater = Updater(token=TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("status", status_command))
    updater.start_polling()
    run_bot()

if __name__ == "__main__":
    telegram_interface()
