import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext
from global_vars import check_channels, file_ids, admins, await_time
from CMDHandle import delete_message_later
from admin import load_user_ids, save_user_ids


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    
    #-------------send_file------------
    data = query.data.split(':')
    command = data[0]
    value = data[1] if len(data) > 1 else None
    user_id = query.from_user.id
    join_channel = []
    if command == "send_file":
        for channel in check_channels.keys():
            try:
                chat_member = await context.bot.get_chat_member(chat_id=f"@{channel}", user_id=user_id)
                if chat_member.status not in ['member', 'administrator', 'creator']:
                    join_channel.append([InlineKeyboardButton(f"{check_channels[channel]['title']}", url=f"https://t.me/{channel}")])
            except Exception as e:
                print(f"Error checking membership for {channel}: {e}")
    
        if join_channel:
            join_channel.append([InlineKeyboardButton("عضو شدم", callback_data=f"send_file:{value}")])
            reply_markup = InlineKeyboardMarkup(join_channel)
            try: 
                await query.edit_message_reply_markup(reply_markup=reply_markup)
            except:
                print("warnning err0")
        else:
            await query.delete_message()
            if int(value) in file_ids:
                message = await context.bot.send_document(chat_id=user_id, document=file_ids[int(value)]["file_id"], caption=file_ids[int(value)]["caption"])
                await query.message.reply_text(f"این پیام بعد {await_time} ثانیه حذف میشود")
                asyncio.create_task(delete_message_later(context, update.effective_chat.id,message.message_id))


            else:
                await query.message.reply_text("فایل وجود ندارد")
    #-------------add_file------------
    if query.data == "add_file":
        await query.edit_message_reply_markup()
        context.user_data["awaiting_file"] = True
        await query.edit_message_text("فایل را ارسال کنید:")
        

async def handle_file(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    file = update.message.document
    try:
        d = context.user_data["awaiting_file"]
    except:
        context.user_data["awaiting_file"] = False
    if context.user_data["awaiting_file"] and file and str(chat_id) in admins:
        context.user_data["awaiting_file"] = False
        file_id = file.file_id
        id = len(file_ids) + 1
        file_ids.update({id:{"file_id":file_id,"caption": "."}})
        context.user_data["file_data_added"] = {"id": id, "file_id": file_id}
        context.user_data["awating_caption"] = True
        await update.message.reply_text("کپشن فایل را بنویسید:")
    
    
    


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    received_text = update.message.text
    if received_text == "مدیریت فایل":
        keyboard = [
            [InlineKeyboardButton("افزودن فایل", callback_data="add_file")],
            
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"یکی از گزینه های زیر را انتخاب کنید:", reply_markup=reply_markup)

    try:
        d = context.user_data["awating_caption"]
    except:
        context.user_data["awating_caption"] = False
   
    if context.user_data["awating_caption"] and received_text:
        id = context.user_data["file_data_added"]["id"]
        file_id = context.user_data["file_data_added"]["file_id"]
        file_ids.update({id:{"file_id":file_id,"caption":received_text }})
        bot_id = "Hfftyyggbot"
        await update.message.reply_text("کپشن اضافه شد")
        context.user_data["awating_caption"] = False
        await update.message.reply_text(f"ایدی فایل : {id}\n لینک فایل: \n https://t.me/{bot_id}?start={id}")

    if received_text == "ارسال پیام به همه":
        context.user_data["send_message_to_all"] = True
        await update.message.reply_text("پیام مورد نظر را ارسال کنید")

    if context.user_data["send_message_to_all"]:

        if not str(update.message.from_user.id) in admins:
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
        context.user_data["send_message_to_all"] = False
        