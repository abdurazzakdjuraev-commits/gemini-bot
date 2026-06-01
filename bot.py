import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
BOT_TOKEN = "8685024177:AAE_zWsRAOUGnyT7xqHnrmOuQ2ibZkI7gdc"
GEMINI_API_KEY = "AQ.Ab8RN6LIUZkG-TAUbkSeUY17Xj7iKvPPAAPaJdQ_BIit5Vn_YA"
CHANNEL = "@Fakt_uz12"
CHANNEL_LINK = "https://t.me/Fakt_uz12"
async def check_sub(uid, ctx):
    try:
        m = await ctx.bot.get_chat_member(chat_id=CHANNEL, user_id=uid)
        return m.status in ["member","administrator","creator"]
    except:
        return False
def kb():
    return InlineKeyboardMarkup([[InlineKeyboardButton("📢 Obuna bo'lish", url=CHANNEL_LINK)],[InlineKeyboardButton("✅ Tekshir", callback_data="chk")]])
async def start(u: Update, ctx):
    if await check_sub(u.effective_user.id, ctx):
        await u.message.reply_text("Salom! Savolingizni yozing 🤖")
    else:
        await u.message.reply_text("Kanalga obuna bo'ling!", reply_markup=kb())
async def chk(u: Update, ctx):
    await u.callback_query.answer()
    if await check_sub(u.effective_user.id, ctx):
        await u.callback_query.edit_message_text("✅ Tasdiqlandi! Savolingizni yozing 🤖")
    else:
        await u.callback_query.edit_message_text("❌ Hali obuna bo'lmadingiz!", reply_markup=kb())
async def msg(u: Update, ctx):
    if not await check_sub(u.effective_user.id, ctx):
        await u.message.reply_text("Obuna bo'ling!", reply_markup=kb())
        return
    await ctx.bot.send_chat_action(u.effective_chat.id, "typing")
    async with httpx.AsyncClient() as client:
        r = await client.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}",json={"contents":[{"parts":[{"text":u.message.text}]}]},timeout=30)
    try:
        reply = r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        reply = "Xatolik yuz berdi."
    await u.message.reply_text(reply[:4096])
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(chk, pattern="chk"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg))
print("Bot ishga tushdi!")
app = Application.builder().token(BOT_TOKEN)build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(chk, pattern="chk"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, xabar))

print("Bot ishga tushdi!")
app.run_polling()
