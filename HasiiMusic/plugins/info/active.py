# ==============================================================================
# active.py - Active Voice Chats Command (Sudo Only)
# ==============================================================================
# This plugin shows statistics about active voice chats where the bot is playing.
#
# Commands:
# - /ac - Show count of active voice chats
#
# Only sudo users can use these commands.
# ==============================================================================

import os
from pyrogram import filters, types
from HasiiMusic import app, db, lang, queue


@app.on_message(filters.command(["ac"]) & app.sudo_filter)
@lang.language()
async def _ac(_, m: types.Message):
    # Auto-delete command message
    try:
        await m.delete()
    except Exception:
        pass
    
    if not db.active_calls:
        return await m.reply_text(m.lang["vc_empty"])

    return await m.reply_text(m.lang["vc_count"].format(len(db.active_calls)))

