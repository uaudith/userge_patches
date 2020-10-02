# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

from typing import Union, Tuple, Optional
from userge import userge, Message, Config
from userge.utils import parse_buttons, get_file_id_and_ref

Channel = userge.getCLogger(__name__)


@userge.on_cmd('cbutton', about={
    'header': "Create Posts with Inline Buttons",
    'flags': {
        '-bot': "Force the bot to post the message"
    },
    'usage': "{tr}cbutton [content | as a reply]: creates a post\n",
    'content': "<code>[name][buttonurl:link]</code> - <b>add a url button</b>\n"
               "<code>[name][buttonurl:link:same]</code> - <b>add a url button to same row</b>"
})
def cBtn(message: Message):
    note, kbrdMkup = parse_buttons(
        message.input_or_reply_str
    )
    mediaids: Union[Tuple[Optional[str], Optional[str]], None] = None
    if message.reply_to_message.media:
        mediaids = get_file_id_and_ref(message.reply_to_message)
    elif message.media:
        mediaids = get_file_id_and_ref(message)
    if not mediaids:
        await message.delete()
        await userge.bot.send_message(
            message.chat.id,
            note,
            reply_markup=kbrdMkup
        )
        return

    if not message.client.is_bot:
        await message.delete()
        _tempMsg = await userge.bot.send_cached_media(
            Config.LOG_CHANNEL_ID,
            mediaids[0],
            file_ref=mediaids[1],
            caption=note,
            reply_markup=kbrdMkup
        )
    else:
        _tempMsg = await userge.bot.send_cached_media(
            message.chat.id,
            mediaids[0],
            file_ref=mediaids[1],
            caption=note,
            reply_markup=kbrdMkup
        )
