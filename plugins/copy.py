import os
import time
import asyncio
import datetime
from config import Config

from pyrogram.errors import FloodWait
from pyrogram import Client, filters

class AsyncIter:    
    def __init__(self, items):    
        self.items = items    

    async def __aiter__(self):    
        for item in self.items:    
            yield item  

    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration as e:
            raise StopAsyncIteration from e



@Client.on_message(filters.media)
async def forward(bot, update):
    try:
        await bot.copy_message(
            chat_id=Config.TO_CHANNEL_,
            from_chat_id=update.chat.id,
            message_id=update.message_id,
            caption=update.caption
        )
    except FloodWait as e:
        time.sleep(e.x)


@Client.on_message(filters.private & filters.command("forward"))
async def forward(bot, update):
    try:
        try:
            start_time = datetime.datetime.now()
            txt = await update.reply_text(text="Forward Started!")
            text = await bot.send_message(Config.FROM_CHANNEL, ".")
            last_msg_id = text.message_id
            await text.delete()
            success = 0
            fail = 0
            total = 0
            empty=0
            total_messages = (range(1,last_msg_id))
            for i in range(Config.START_FROM ,len(total_messages), 200):
                channel_posts = AsyncIter(await bot.get_messages(Config.FROM_CHANNEL, total_messages[i:i+200]))
                async for message in channel_posts:
                    if message.video or message.audio or message.document or message.photo:
                        try:
                            await message.copy(Config.TO_CHANNEL)
                            success+=1
                        except Exception as e:
                            fail+=1
                            await bot.send_message(update.from_user.id,f"this msg_id {message.message_id} give error {e}")
                            time.sleep(2)
                    else:
                        empty+=1
                    total+=1
                    
                    if total % 5 == 0:
                        msg = f"Batch forwarding in Process !\n\nTotal: {total}\nSuccess: {success}\nFailed: {fail}\nEmpty: {empty}"
                        await txt.edit((msg))
                    time.sleep(2)
        
        except FloodWait as e:
            time.sleep(e.x)
    
    except Exception as e:
        await txt.reply_text(f"{e}")
    
    finally:
        end_time = datetime.datetime.now()
        await asyncio.sleep(4)
        t = end_time - start_time
        time_taken = str(datetime.timedelta(seconds=t.seconds))
        msg = f"Batch Forwarding Completed!\n\nTime Taken - `{time_taken}`\n\nTotal: `{total}`\nSuccess: `{success}`\nFailed: `{fail}`\nEmpty: `{empty}`"
        await txt.edit(msg)    
