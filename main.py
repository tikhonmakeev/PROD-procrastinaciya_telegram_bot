import asyncio
import json
import logging
import os
import sys

import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from aiohttp import ClientSession

server_url = "HERE_IS_SERVER_URL"
TOKEN = "HERE IS BOTKEY"  # release bot key
bot = Bot(TOKEN)
bot_id = "telegram"

dp = Dispatcher()
folder = os.path.expanduser('~/uploads')


@dp.channel_post(F.text.startswith("/code"))
async def channel_verify(message: types.Message) -> None:
    data = message.text.split()
    if len(data) != 2:
        return
    code = data[1]
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{server_url}/auth_bot',
                                data=json.dumps({
                                    "chat_name": message.chat.full_name,
                                    "avatar_uri": message.chat.photo.small_file_id if message.chat.photo is not None
                                    else "",
                                    "chat_id": message.chat.id,
                                    "verification_key": code,
                                    "bot_id": bot_id
                                }),
                                headers={'Content-type': 'application/json'},
                                ) as _:
            pass
    await message.delete()


@dp.message(F.text.startswith("/code"))
async def pm_verify(message: types.Message) -> None:
    data = message.text.split()
    if len(data) != 2:
        await message.answer(
            "Вам нужно ввести '/code (здесь код)'.\nУбедитесь, что между командой и кодом есть пробел, "
            "а между символами кода пробелов нет."
        )
        return
    code = data[1]
    async with aiohttp.ClientSession() as session:
        query_data = json.dumps({
            "chat_name": message.chat.full_name,
            "telegram_user_id": message.from_user.id,
            "avatar_uri": message.chat.photo.small_file_id if message.chat.photo is not None
            else "",
            "chat_id": message.chat.id,
            "verification_key": code,
            "bot_id": bot_id
        })

        if message.chat.type == "private":

            async with session.post(f'{server_url}/auth_user',
                                    data=query_data,
                                    headers={'Content-type': 'application/json'},
                                    ) as _:
                pass
        else:

            async with session.post(f'{server_url}/auth_bot',
                                    data=query_data,
                                    headers={'Content-type': 'application/json'},
                                    ) as _:
                pass
    await message.delete()


async def bot_tasks():
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(f'{server_url}/get_bot_actions/{bot_id}') as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        await get_updates(data, session)
            except Exception as e:
                logging.error(e)
            await asyncio.sleep(5)


async def get_updates(data, session: ClientSession):
    for data in data["data"]:
        # if data["action"] == "send_message":
        successful = True
        message = "OK"
        real_message = None
        try:
            only_images = True
            text = data["message"]
            print(text)
            if len(data["attachments"]):
                attachments = []
                for i in data["attachments"]:
                    path = f"{folder}/{i['file_id']}"
                    if i["is_image"]:
                        attachments.append(
                            types.InputMediaPhoto(media=FSInputFile(path, i['file_name']), caption=text,
                                                  parse_mode=ParseMode.MARKDOWN_V2)
                        )
                    else:
                        attachments.append(
                            types.InputMediaDocument(media=FSInputFile(path, i['file_name']), caption=text,
                                                     parse_mode=ParseMode.MARKDOWN_V2)
                        )
                        only_images = False
                    data['message'] = None
                if only_images and len(attachments) == 1:
                    real_message = await bot.send_photo(data["telegram_chat_id"], attachments[0].media, caption=text,
                                                        parse_mode=ParseMode.MARKDOWN_V2)
                else:
                    real_message = await bot.send_media_group(data["telegram_chat_id"], attachments)
            else:
                real_message = await bot.send_message(data["telegram_chat_id"], text,
                                                      parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            print(e)
            successful = False
            message = str(e)
        print(real_message)
        if isinstance(real_message, list):
            real_message = real_message[0].message_id
        elif real_message is not None:
            real_message = real_message.message_id
        async with session.post(f'{server_url}/confirm',
                                data=json.dumps({
                                    "message_id": data["message_id"],
                                    "is_successful": successful,
                                    "message": message,
                                    "real_message_id": real_message,
                                }),
                                headers={'Content-type': 'application/json'}) as _:
            pass


@dp.message_reaction_count()
async def message_reaction_count_handler(message_reaction_count: types.MessageReactionCountUpdated):
    reactions = {
        "bot_id": bot_id,
        "message_id": message_reaction_count.message_id,
        "reactions": [{i.type.emoji: i.total_count} for i in message_reaction_count.reactions]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{server_url}/reactions', data=json.dumps(reactions),
                                headers={'Content-type': 'application/json'}) as _:
            pass


async def main() -> None:
    asyncio.ensure_future(bot_tasks())
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
