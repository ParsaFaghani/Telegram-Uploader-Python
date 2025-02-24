import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler, ContextTypes
from global_vars import file_ids, admins, check_channels, await_time


async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    args = context.args
    if str(chat_id) in admins:
        keyboard = [
        ["مدیریت فایل", 'Button 2'],
        ['Button 3', 'Button 4']
    ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
        await update.message.reply_text('خوش امدید', reply_markup=reply_markup)
        


    if args:
        user_id = update.message.from_user.id
        param = int(args[0])
        join_channel = []
        for channel in check_channels.keys():
            try:
                chat_member = await context.bot.get_chat_member(chat_id=f"@{channel}", user_id=user_id)
                if chat_member.status not in ['member', 'administrator', 'creator']:
                    join_channel.append([InlineKeyboardButton(f"{check_channels[channel]['title']}", url=f"https://t.me/{channel}")])
            except Exception as e:
                print(f"Error checking membership for {channel}: {e}")

        if not join_channel:
                
                if param in file_ids:
                    message = await context.bot.send_document(chat_id=chat_id, document=file_ids[param]["file_id"], caption=file_ids[param]["caption"])
                    await update.message.reply_text(f"این پیام بعد {await_time} ثانیه حذف میشود")
                    
                    asyncio.create_task(delete_message_later(context, update.effective_chat.id, message.message_id))

                    
                    
                else:
                    await update.message.reply_text("فایل پیدا نشد")
        else:
                join_channel.append([InlineKeyboardButton("عضو شدم", callback_data=f"send_file:{param}")])
                reply_markup = InlineKeyboardMarkup(join_channel)
                await update.message.reply_text("شما برای استفاده از ربات باید عضو کانال های زیر باشید:", reply_markup=reply_markup)
    else:
        await update.message.reply_text('No parameter found.')
        



async def delete_message_later(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int) -> None:
    # تعیین مدت زمان (در اینجا 10 ثانیه) برای حذف پیام
    await asyncio.sleep(await_time)
    
    # حذف پیام
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        print(f"Error deleting message: {e}")
