from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler, ContextTypes
from global_vars import file_ids, admins, check_channels





  
  
  

async def send_all_files(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    if str(chat_id) in admins:
        for file_id in file_ids:
            await context.bot.send_document(chat_id=chat_id, document=file_ids[file_id]["id"],caption=file_id)

