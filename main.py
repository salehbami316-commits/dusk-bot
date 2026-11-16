import os, json, threading
from datetime import datetime, timedelta
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot is Live!"

def load_users():
    try:
        with open("users.json","r") as f:
            return json.load(f)
    except:
        return {}

def save_users(d):
    with open("users.json","w",encoding="utf-8") as f:
        json.dump(d,f,ensure_ascii=False)

def is_subscribed(uid):
    u = load_users()
    if str(uid) not in u:
        return False
    try:
        return datetime.now() < datetime.fromisoformat(u[str(uid)]["expire"])
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if is_subscribed(uid):
        await update.message.reply_text("✅ اشتراكك فعال! اهلا فيك")
        return
    await update.message.reply_text(f"🚀 مرحبا!\n\n💳 CliQ: S198611\nالاسم: Saleh Bani\n💵 10د / شهر\n\nID تبعك: {uid}\nبعد الدفع ارسل الـ ID للادمن")

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("استخدم: /approve USER_ID 30")
        return
    tid = context.args[0]
    days = int(context.args[1]) if len(context.args) > 1 else 30
    users = load_users()
    exp = datetime.now() + timedelta(days=days)
    users[str(tid)] = {"expire": exp.isoformat()}
    save_users(users)
    await update.message.reply_text(f"✅ فعلت {tid} لـ {days} يوم")
    try:
        await context.bot.send_message(chat_id=int(tid), text=f"🎉 تم تفعيل اشتراكك {days} يوم!")
    except:
        pass

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(str(update.effective_user.id))

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CommandHandler("myid", myid))
    print("Bot starting...")
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)
