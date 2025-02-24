from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler, ContextTypes
from global_vars import file_ids, admins, check_channels, USER_IDS_FILE
import json
import os

def load_user_ids():
    if not os.path.exists(USER_IDS_FILE):
        return []
    try:
        with open(USER_IDS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_user_ids(user_ids):
    with open(USER_IDS_FILE, 'w') as f:
        json.dump(user_ids, f)
  

async def sendtoall(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("ok")
    if context.user_data["send_message_to_all"]:

        if not update.message.from_user.id in admins:
            await update.message.reply_text('شما اجازه انجام این کار را ندارید.')
            return
        
        user_ids = load_user_ids()
        message = update.message
        for user_id in user_ids:
            try:
                if message.text:
                    await context.bot.send_message(chat_id=user_id, text=message.text)
                elif message.photo:
                    await context.bot.send_photo(chat_id=user_id, photo=message.photo[-1].file_id, caption=message.caption)
                elif message.video:
                    await context.bot.send_video(chat_id=user_id, video=message.video.file_id, caption=message.caption)
                elif message.document:
                    await context.bot.send_document(chat_id=user_id, document=message.document.file_id, caption=message.caption)
                elif message.audio:
                    await context.bot.send_audio(chat_id=user_id, audio=message.audio.file_id, caption=message.caption)
                elif message.voice:
                    await context.bot.send_voice(chat_id=user_id, voice=message.voice.file_id, caption=message.caption)
                elif message.sticker:
                    await context.bot.send_sticker(chat_id=user_id, sticker=message.sticker.file_id)
                elif message.animation:
                    await context.bot.send_animation(chat_id=user_id, animation=message.animation.file_id, caption=message.caption)
            except Exception as e:
                print(f"خطا در ارسال پیام به {user_id}: {e}")
    


async def send_all_files(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    if str(chat_id) in admins:
        for file_id in file_ids:
            await context.bot.send_document(chat_id=chat_id, document=file_ids[file_id]["file_id"],caption=file_id)

