import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

WELCOME = """Приветствую! 👋

Если тебя интересует индивидуальная работа со мной, ниже актуальные форматы:

🔥 Индивидуальное ведение — 60$ / 5000₽ в месяц

В ведение входит:
— составление программы тренировок и плана питания под твои цели
— еженедельный отчёт по форме и корректировка планов
— разбор техники выполнения упражнений
— разбор анализов
— консультация со мной по всем вопросам 24/7

📋 Индивидуальный план тренировок или питания — 20$ / 1000₽

🔥 Тренировки + питание — 30$ / 1700₽

💬 Индивидуальная онлайн-консультация — 40$ / 2500₽

Все планы составляются индивидуально под твои цели и задачи.

⏱ Срок составления — до 6 часов после оплаты.

Выбери интересующий тебя формат 👇"""

def menu():
    keyboard = [
        [InlineKeyboardButton("🔥 Индивидуальное ведение", callback_data="coaching")],
        [InlineKeyboardButton("📋 Тренировки + питание", callback_data="plans")],
        [InlineKeyboardButton("💬 Онлайн-консультация", callback_data="consultation")],
        [InlineKeyboardButton("💰 Все услуги и цены", callback_data="prices")],
        [InlineKeyboardButton("📞 Связаться со мной", callback_data="contact")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME, reply_markup=menu())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    texts = {
        "coaching": """🔥 Индивидуальное ведение

60$ / 5000₽ в месяц

Включает:
— программу тренировок и план питания
— еженедельный отчёт и корректировку планов
— разбор техники упражнений
— разбор анализов
— консультацию со мной 24/7

⏱ Срок составления — до 6 часов после оплаты.""",

        "plans": """📋 Индивидуальные планы

План тренировок или питания — 20$ / 1000₽

Тренировки + питание — 30$ / 1700₽

Все планы составляются индивидуально под твои цели.

⏱ Срок составления — до 6 часов после оплаты.""",

        "consultation": """💬 Индивидуальная онлайн-консультация

Стоимость — 40$ / 2500₽

На консультации разберём интересующие тебя вопросы и подберём оптимальный вариант работы.""",

        "prices": WELCOME,

        "contact": """📞 Связь со мной

Если хочешь начать работу или остались вопросы — напиши мне напрямую.

Твой Telegram: @egorrrr05"""
    }

    await query.edit_message_text(
        texts[query.data],
        reply_markup=menu()
    )

async def main():
    token = os.environ.get("BOT_TOKEN")

    if not token:
        raise ValueError("Не найден BOT_TOKEN")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    print("Бот запущен!")

    try:
        await asyncio.Event().wait()
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
