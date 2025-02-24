from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from CMDHandle import start
from global_vars import TOKEN, check_channels, file_ids
from handler import handle_text, button, handle_file
from admin import sendtoall





def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, sendtoall))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()
()
if __name__ == '__main__':
    main()