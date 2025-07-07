from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from datetime import datetime, timedelta
import sqlite3
import re

BOT_TOKEN = '7102402149:AAGFa494i7ABbdly9flzFRUGW_UwvdzVn2c'

LINK_REGEX = r'https?://\S+'
MAX_MESSAGES = 3
TIME_WINDOW = timedelta(seconds=10)
user_message_log = {}

# Connect to SQLite DB
conn = sqlite3.connect('spam_guard.db', check_same_thread=False)
cursor = conn.cursor()

def get_spam_keywords():
    cursor.execute("SELECT keyword FROM spam_keywords")
    return [row[0] for row in cursor.fetchall()]

def log_to_db(username, user_id, message, action):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # local time string
    cursor.execute('''
        INSERT INTO spam_logs (username, user_id, message, action, log_time)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, user_id, message, action, now))
    conn.commit()

async def detect_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user = update.message.from_user
    user_id = user.id
    username = user.username or f"id_{user_id}"
    chat_id = update.message.chat_id
    text = update.message.text.lower()
    now = datetime.now()

    user_message_log.setdefault(user_id, []).append(now)
    user_message_log[user_id] = [t for t in user_message_log[user_id] if now - t < TIME_WINDOW]

    try:
        member = await context.bot.get_chat_member(chat_id, user_id)
        is_admin = member.status in ['administrator', 'creator']
    except:
        is_admin = False

    spam_keywords = get_spam_keywords()

    is_spam = (
        any(kw in text for kw in spam_keywords)
        or re.search(LINK_REGEX, text)
        or len(user_message_log[user_id]) > MAX_MESSAGES
    )

    action_taken = ""
    if is_spam:
        await update.message.delete()
        action_taken = "Message deleted"

        if not is_admin:
            await context.bot.restrict_chat_member(
                chat_id, user_id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=now + timedelta(minutes=1)
            )
            await context.bot.send_message(chat_id, f"🚨 Spam alert: @{username} muted for 1 minute.")
            action_taken += " + User muted"
        else:
            await context.bot.send_message(chat_id, f"⚠️ Admin @{username}'s spam message deleted.")
            action_taken += " (admin not muted)"

        log_to_db(username, user_id, text, action_taken)
        print(f"[LOGGED] {action_taken} | User: @{username}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    print("🚀 SpamGuardHelperBot running with SQLite...")
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, detect_spam))
    app.run_polling()
