import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
MINI_APP_URL = os.environ.get("MINI_APP_URL")

LANG_KEYBOARD = InlineKeyboardMarkup([[
    InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
    InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
    InlineKeyboardButton("🇮🇱 עברית", callback_data="lang_he"),
]])

TEXTS = {
    "ru": ("🏠 *Israel Property*\n\nДоска недвижимости Израиля.\n\nНажми кнопку ниже 👇", "🏠 Открыть каталог"),
    "en": ("🏠 *Israel Property*\n\nReal estate in Israel.\n\nTap below 👇", "🏠 Open catalog"),
    "he": ("🏠 *Israel Property*\n\nנדל\"ן בישראל.\n\nלחץ למטה 👇", "🏠 פתח קטלוג"),
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌐 Выберите язык / Choose language / בחר שפה:", reply_markup=LANG_KEYBOARD)

async def lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    l = q.data.replace("lang_", "")
    text, btn = TEXTS.get(l, TEXTS["en"])
    kb = InlineKeyboardMarkup([[InlineKeyboardButton(btn, web_app=WebAppInfo(url=MINI_APP_URL))]])
    await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(lang, pattern="^lang_"))
print("Bot started")
app.run_polling()
