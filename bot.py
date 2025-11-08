import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

# 🔑 Dán token thật của bot bạn vào đây
BOT_TOKEN = "8464821991:AAHXkTKp9XhPltxfaDSSladUQ82dMG6LQTw"

# 👤 ID Telegram của bạn
OWNER_ID = 5523799948

# 🔗 Link bạn cung cấp
THREAD_LINK = "https://www.threads.com/@keo.bong.free?igshid=NTc4MTIwNjQ2YQ=="
VIP_LINK    = "https://t.me/adthanhsang"
LINK1       = "https://www.bongvip25.com/register.html?affiliateCode=ko3wd"
LINK2       = "https://ap207.bongvipvn.wiki/"

TITLE = "⚽ Kèo bóng Free ⚽"

# Dùng biến toàn cục để lưu ID tin nhắn cũ
last_message_id = None

def kb_main():
    rows = [
        [InlineKeyboardButton("📍Thread AD ✅", url=THREAD_LINK)],
        [InlineKeyboardButton("📍Đăng Ký Nhóm V.I.P 🏆 200k", url=VIP_LINK)],
        [InlineKeyboardButton("📍WEB Bongvip25 💸", callback_data="web_menu")],
    ]
    return InlineKeyboardMarkup(rows)

def kb_web_sub():
    rows = [
        [InlineKeyboardButton("⚽ Link 1", url=LINK1)],
        [InlineKeyboardButton("⚽ Link 2", url=LINK2)],
        [InlineKeyboardButton("⬅️ Quay lại", callback_data="back_main")],
    ]
    return InlineKeyboardMarkup(rows)

# /whoami
async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id if update.effective_user else None
    await update.message.reply_text(f"Your user_id: {uid}")

# Xử lý khi bạn nhắn trong nhóm
async def on_group_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_message_id

    if update.effective_user and update.effective_user.id == OWNER_ID:
        if update.message and not update.message.text.startswith("/"):

            # Nếu có tin cũ thì xóa nó
            if last_message_id:
                try:
                    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=last_message_id)
                except:
                    pass  # bỏ qua nếu tin cũ đã bị xóa

            # Gửi tin mới
            msg = await update.message.reply_text(TITLE, reply_markup=kb_main())

            # Lưu lại ID tin nhắn mới nhất
            last_message_id = msg.message_id

# Xử lý nút submenu
async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "web_menu":
        try:
            await query.edit_message_text(TITLE, reply_markup=kb_web_sub())
        except:
            pass

    elif query.data == "back_main":
        try:
            await query.edit_message_text(TITLE, reply_markup=kb_main())
        except:
            pass

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("whoami", whoami))
    app.add_handler(MessageHandler(filters.ChatType.GROUPS & filters.TEXT, on_group_text))
    app.add_handler(CallbackQueryHandler(on_button))

    print("🤖 Bot đang chạy... (ấn Ctrl + C để tắt)")
    app.run_polling()

if __name__ == "__main__":
    main()
