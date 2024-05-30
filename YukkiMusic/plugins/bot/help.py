#
# Copyright (C) 2024-present by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
#

import random
import re
from typing import Union

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import BANNED_USERS, PHOTO, START_IMG_URL
from strings import get_command, get_string
from YukkiMusic import HELPABLE, app
from YukkiMusic.utils.database import get_lang, is_commanddelete_on
from YukkiMusic.utils.decorators.language import LanguageStart
from YukkiMusic.utils.inline.help import private_help_panel
from YukkiMusic.utils.inlinefunction import paginate_modules

### Command
HELP_COMMAND = get_command("HELP_COMMAND")


@app.on_message(filters.command(HELP_COMMAND) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(
    client: app, update: Union[types.Message, types.CallbackQuery]
):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        text, keyboard = await help_parser(update.from_user.mention)
        await update.edit_message_text(text, reply_markup=keyboard)
    else:
        chat_id = update.chat.id
        if await is_commanddelete_on(update.chat.id):
            try:
                await update.delete()
            except:
                pass
        language = await get_lang(chat_id)
        _ = get_string(language)
        text, keyboard = await help_parser(update.from_user.mention)
        if START_IMG_URL:
            await update.reply_photo(
                photo=START_IMG_URL,
                caption=text,
                reply_markup=keyboard,
            )

        else:
            await update.reply_photo(
                photo=random.choice(PHOTO),
                caption=_["help_1"],
                reply_markup=keyboard,
            )


@app.on_message(filters.command(HELP_COMMAND) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
        f"""ʜᴇʟʟᴏ {name},

ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ.

ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs sᴛᴀʀᴛs ᴡɪᴛʜ :-  /
""",
        keyboard,
    )


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query: Union[types.InlineQuery, types.CallbackQuery]):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back\((\d+)\)", query.data)
    create_match = re.match(r"help_create", query.data)

    top_text = f"""ʜᴇʟʟᴏ {query.from_user.mention},

ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ.

ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs sᴛᴀʀᴛs ᴡɪᴛʜ :-  /
"""

    if mod_match:
        module = mod_match.group(1)
        prev_page_num = int(mod_match.group(2))
        text = (
            f"**ʜᴇʀᴇ ɪs ᴛʜᴇ ʜᴇʟᴘ ғᴏʀ** {HELPABLE[module].__MODULE__}:\n"
            + HELPABLE[module].__HELP__
        )

        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="↪️ Back", callback_data=f"help_back({prev_page_num})"
                    ),
                    InlineKeyboardButton(text="🔄 Close", callback_data="close"),
                ],
            ]
        )

        if query.inline_message_id:
            await query.edit_inline_text(
                inline_message_id=query.inline_message_id,
                text=text,
                reply_markup=key,
                disable_web_page_preview=True,
            )
        else:
            await query.message.edit(
                text=text,
                reply_markup=key,
                disable_web_page_preview=True,
            )

    elif home_match:
        await app.send_message(
            query.from_user.id,
            text=home_text_pm,
            reply_markup=InlineKeyboardMarkup(out),
        )

    elif prev_match:
        curr_page = int(prev_match.group(1))
        if query.inline_message_id:
            await query.edit_inline_text(
                inline_message_id=query.inline_message_id,
                text=top_text,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page, HELPABLE, "help")
                ),
                disable_web_page_preview=True,
            )
        else:
            await query.message.edit(
                text=top_text,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page, HELPABLE, "help")
                ),
                disable_web_page_preview=True,
            )

    elif next_match:
        next_page = int(next_match.group(1))
        if query.inline_message_id:
            await query.edit_inline_text(
                inline_message_id=query.inline_message_id,
                text=top_text,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page, HELPABLE, "help")
                ),
                disable_web_page_preview=True,
            )
        else:
            await query.message.edit(
                text=top_text,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page, HELPABLE, "help")
                ),
                disable_web_page_preview=True,
            )

    elif back_match:
        prev_page_num = int(back_match.group(1))
        if query.inline_message_id:
            await query.edit_inline_text(
                inline_message_id=query.inline_message_id,
                text=top_text,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(prev_page_num, HELPABLE, "help")
                ),
                disable_web_page_preview=True,
            )
        else:
            await query.message.edit(
                text=top_text,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(prev_page_num, HELPABLE, "help")
                ),
                disable_web_page_preview=True,
            )

    elif create_match:
        text, keyboard = await help_parser(query)
        if query.inline_message_id:
            await query.edit_inline_text(
                inline_message_id=query.inline_message_id,
                text=text,
                reply_markup=keyboard,
                disable_web_page_preview=True,
            )
        else:
            await query.message.edit(
                text=text,
                reply_markup=keyboard,
                disable_web_page_preview=True,
            )

    await client.answer_callback_query(query.id)
