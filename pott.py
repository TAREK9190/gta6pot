from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import datetime
from flask import Flask
from threading import Thread

# إعداد Flask لتشغيل البوت 24/7
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "<h1>✅ البوت شغال 24 ساعة</h1>"

def run():
    flask_app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 🔐 توكن البوت
TOKEN = '7915942877:AAF1Yr3N_MtWUSws8uiIvHnqRa6-siswXME'

# التاريخ المستهدف
target_date = datetime.datetime(2026, 5, 25, 0, 0, 0)

# الرسالة المخصصة
custom_message = """<b>اهلا فيكم جميعا🖤</b>
<b>هذا عد تنازلي الى حين اصدار لعبة GTA 6 🤩</b>

<b>كل يوم راح ينقص يوم من العداد ⏳
تبقى على اصدار GTA6 فقط ⬇️</b>
"""

# دالة حساب الأيام
def get_remaining():
    now = datetime.datetime.now()
    diff = target_date - now
    if diff.total_seconds() <= 0:
        return "<b>🎉 تم الوصول إلى التاريخ المحدد!</b>"
    days = diff.days
    return f"<b>الأيـام 🗓: {days}</b><b> . </b>"

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔄 تحديث العد التنازلي", callback_data='refresh')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    countdown_text = get_remaining()
    await update.message.reply_text(
        f"{custom_message}\n\n{countdown_text}",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

# زر التحديث
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    countdown_text = get_remaining()
    keyboard = [[InlineKeyboardButton("🔄 تحديث العد التنازلي", callback_data='refresh')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        f"{custom_message}\n\n{countdown_text}",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

# الرد على الكلمات أو العبارات
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    keywords = [
        "تحديث العد", "العد التنازلي", "عد تنازلي", "gta6", "gta 6",
        "قراند 6", "قراند6", "كم باقي على gta6", "كم باقي على قراند6",
        "كم باقي على قراند 6", "متى تصدر قراند 6", "متى تصدر قراند6",
        "موعد نزول قراند6", "موعد نزول قراند 6"
    ]
    if text in [k.lower() for k in keywords]:
        keyboard = [[InlineKeyboardButton("🔄 تحديث العد التنازلي", callback_data='refresh')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        countdown_text = get_remaining()
        await update.message.reply_text(
            f"{custom_message}\n\n{countdown_text}",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )

# ✅ تشغيل البوت
if __name__ == "__main__":
    keep_alive()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button))
    print("✅ البوت شغال الآن...")
    app.run_polling()