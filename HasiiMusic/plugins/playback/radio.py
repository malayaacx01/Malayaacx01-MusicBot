# ==============================================================================
# radio.py - Live Radio
# ==============================================================================
# UI and logic for streaming 50+ live radio stations.
# ==============================================================================

import asyncio
import logging
import time

from pyrogram import enums, errors, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from HasiiMusic import tune, app, config, db, lang, queue
from HasiiMusic.helpers import buttons, utils

# Set up logging
LOGGER = logging.getLogger(__name__)

# Dictionary of radio stations with their stream URLs

# Radio stations organized by categories
RADIO_CATEGORIES = {
    "🇱🇰 ꜱʀɪ ʟᴀɴᴋᴀɴ ʀᴀᴅɪᴏ": {
        "ꜱʟʙᴄ ʀᴀᴅɪᴏ": "http://220.247.227.20:8000/RSLstream",
        "ꜱɪʏᴀᴛʜᴀ ꜰᴍ": "https://srv01.onlineradio.voaplus.com/siyathafm",
        "ɪᴛɴ ꜰᴍ": "https://cp12.serverse.com/proxy/itnfm/stream",
        "ʀʜʏᴛʜᴍ ꜰᴍ": "https://srv01.onlineradio.voaplus.com/rhythmfm",
        "ᴋᴏᴛʜᴍᴀʟᴇ ꜰᴍ": "https://s46.myradiostream.com:11156/listen.mp3",
        "ᴄᴏʟᴏᴜʀ ʀᴀᴅɪᴏ": "https://stream.zeno.fm/uo3gmts0ilivv",
        "ꜰʀᴇᴇ ꜰᴍ": "https://stream.zeno.fm/1tcs4fbw7rquv",
        "ꜱᴇᴛʜ ꜰᴍ": "https://listen.radioking.com/radio/384487/stream/435781",
        "ᴠ ꜰᴍ": "https://dc1.serverse.com/proxy/fmlanka/stream",
        "ꜱɪʀᴀꜱᴀ ꜰᴍ": "http://live.trusl.com:1170/",
        "ʜɪʀᴜ ꜰᴍ": "https://radio.lotustechnologieslk.net:2020/stream/hirufmgarden",
        "ʏ ꜰᴍ": "http://live.trusl.com:1180/",
        "ꜱʜᴀᴀ ꜰᴍ": "https://radio.lotustechnologieslk.net:2020/stream/shaafmgarden",
        "ᴅᴇʀᴀɴᴀ ꜰᴍ": "https://cp12.serverse.com/proxy/fmderana/stream",
        "ɢᴏʟᴅ ꜰᴍ": "https://radio.lotustechnologieslk.net:2020/stream/goldfmgarden",
        "ꜱᴏᴏʀɪʏᴀɴ ꜰᴍ": "https://radio.lotustechnologieslk.net:2020/stream/sooriyanfmgarden",
        "ʙᴇꜱᴛᴄᴏᴀꜱᴛ.ꜰᴍ": "https://streams.radio.co/sea5dddd6b/listen",
        "ʏᴇꜱ ꜰᴍ": "http://live.trusl.com:1160/",
        "ꜱɪᴛʜᴀ ꜰᴍ": "https://stream.streamgenial.stream/cdzzrkrv0p8uv",
        "ʜɪʀᴜ ꜰᴍ ɢᴀʀᴅᴇɴ": "https://radio.lotustechnologieslk.net:2020/stream/hirufmgarden",
        "ꜱᴜɴ ꜰᴍ": "https://radio.lotustechnologieslk.net:2020/stream/sunfmgarden",
        "ꜱʜʀᴇᴇ ꜰᴍ": "https://streamingv2.shoutcast.com/shreefm945",
        "ʀᴀɴ ꜰᴍ": "https://a3.asurahosting.com/listen/ranfm/radio.mp3",
        "ɴᴇᴛʜ ꜰᴍ": "https://cp11.serverse.com/proxy/nethfm/stream",
        "ᴋɪꜱꜱ ꜰᴍ": "https://srv01.onlineradio.voaplus.com/kissfm",
        "ʀᴀɴɢɪʀɪ ꜰᴍ": "https://stream.streamgenial.stream/hwafmr3f4p8uv",
        "ʟᴀᴋʜᴀɴᴅᴀ ʀᴀᴅɪᴏ": "https://cp12.serverse.com/proxy/itnfm?mp=/stream",
        "ɴᴀ ᴅᴀʜᴀꜱᴀ ꜰᴍ": "https://stream-155.zeno.fm/z7q96fbw7rquv",
        "ᴘᴀʀᴀɴɪ ɢᴇᴇ": "http://cast2.citrus3.com:8288/",
    },
    "🇲🇾 ᴍᴀʟᴀʏꜱɪᴀɴ ʀᴀᴅɪᴏ": {
        "ᴘᴇʀᴀᴋ ꜰᴍ": "https://28103.live.streamtheworld.com/PERAK_FMAAC/HLS/playlist.m3u8?id=32979",
        "ɴᴀᴛɪᴏɴᴀʟ ꜰᴍ": "https://22273.live.streamtheworld.com/NASIONAL_FMAAC/HLS/ee0f0bdc-7b91-48bc-84e6-8102f8160e5f/0/playlist.m3u8",
        "ʀᴀᴅɪᴏ ᴍᴜᴢɪᴋ": "https://28093.live.streamtheworld.com/MUZIKFMAAC/HLS/playlist.m3u8?id=32970",
        "ᴋʟ ꜰᴍ": "https://22273.live.streamtheworld.com/KL_FMAAC/HLS/playlist.m3u8?id=32975",
        "ᴍᴜᴛɪᴀʀᴀ ꜰᴍ": "https://28093.live.streamtheworld.com/MUTIARA_FMAAC/HLS/playlist.m3u8?id=32976",
        "ᴘᴇʀʟɪꜱ ꜰᴍ": "https://22283.live.streamtheworld.com/PERLIS_FMAAC/HLS/playlist.m3u8?id=32977",
        "ᴋᴇᴅᴀʜ ꜰᴍ": "https://22283.live.streamtheworld.com/KEDAH_FMAAC/HLS/playlist.m3u8?id=32978",
        "ꜱᴇʟᴀɴɢᴏʀ ꜰᴍ": "https://22283.live.streamtheworld.com/KEDAH_FMAAC/HLS/playlist.m3u8?id=32978",
        "ɴᴇɢᴇʀɪ ꜰᴍ": "https://22253.live.streamtheworld.com/NEGERI_FMAAC/HLS/playlist.m3u8?id=32981",
        "ᴊᴏʜᴏʀ ꜰᴍ": "https://18253.live.streamtheworld.com/JOHOR_FMAAC/HLS/83f9148e-2a93-4439-a401-c586e2bf8dba/0/playlist.m3u8",
        "ʙ ꜰᴍ": "https://n04-us.rcs.revma.com/s91qy9p0zs3vv?rj-ttl=5&rj-tok=AAABnr9n4QQAv7nGNQB1PkuNDA",
        "ᴍᴇʟᴀᴋᴀ ꜰᴍ": "https://28103.live.streamtheworld.com/MELAKA_FMAAC/HLS/playlist.m3u8?id=32983",
        "ʀᴇᴅ ꜰᴍ": "https://28103.live.streamtheworld.com/RED_FMAAC/HLS/playlist.m3u8?id=33005",
        "ᴍɪʀɪ ꜰᴍ": "https://28103.live.streamtheworld.com/MIRI_FMAAC/HLS/playlist.m3u8?id=33009",
        "ᴄᴀᴛꜱ ꜰᴍ": "https://n05-us.rcs.revma.com/51qe53rv0y3vv.m4a?rj-ttl=5&rj-tok=AAABnr-UjPkAvryJ4ZrmFABL9A",
    },
    "📚 ꜱᴛᴜᴅʏ & ꜰᴏᴄᴜꜱ": {
        "ɢʀᴏᴏᴠᴇ ꜱᴀʟᴀᴅ": "https://ice1.somafm.com/groovesalad-128-mp3",
        "ᴅʀᴏɴᴇ ᴢᴏɴᴇ": "https://ice1.somafm.com/dronezone-128-mp3",
        "ꜱᴘᴀᴄᴇ ꜱᴛᴀᴛɪᴏɴ": "https://ice1.somafm.com/spacestation-128-mp3",
        "ᴅᴇᴇᴘꜱᴘᴀᴄᴇ": "https://ice1.somafm.com/deepspaceone-128-mp3",
        "ᴄʟɪǫᴜᴇ ʟᴏᴜɴɢᴇ": "https://ice1.somafm.com/cliqhop-128-mp3",
        "ʟᴜꜱʜ": "https://ice1.somafm.com/lush-128-mp3",
        "ᴄʜɪʟʟʜᴏᴘ ᴍᴜꜱɪᴄ": "https://streams.fluxfm.de/Chillhop/mp3-128",
        "ꜱᴍᴏᴏᴛʜ ᴊᴀᴢᴢ 24/7": "https://mediaserv38.live-streams.nl:18006/stream",
        "ʟᴏꜰɪ ʜɪᴘ-ʜᴏᴘ": "https://streams.fluxfm.de/Chillhop/mp3-128",
    },
    "💻 ᴄᴏᴅɪɴɢ & ᴘʀᴏɢʀᴀᴍᴍɪɴɢ": {
        "ᴄᴏᴅᴇ ʀᴀᴅɪᴏ": "https://coderadio-admin-v2.freecodecamp.org/listen/coderadio/radio.mp3",
        "ɴɪɢʜᴛᴡᴀᴠᴇ ᴘʟᴀᴢᴀ": "https://radio.plaza.one/mp3",
        "ᴅᴇꜰᴄᴏɴ ʀᴀᴅɪᴏ": "https://ice1.somafm.com/defcon-128-mp3",
        "ᴍɪꜱꜱɪᴏɴ ᴄᴏɴᴛʀᴏʟ": "https://ice1.somafm.com/missioncontrol-128-mp3",
        "ᴄʏʙᴇʀɴᴇᴛɪᴄꜱ": "https://ice1.somafm.com/sf1033-128-mp3",
        "ᴄʜɪᴘᴛᴜɴᴇ ʀᴀᴅɪᴏ": "https://relay.chiptunes.cafe/stream",
        "ꜱᴇᴄʀᴇᴛ ᴀɢᴇɴᴛ": "https://ice1.somafm.com/secretagent-128-mp3",
    },
    "🧘 ᴀᴍʙɪᴇɴᴛ & ᴍᴇᴅɪᴛᴀᴛɪᴏɴ": {
        "ᴀᴍʙɪᴇɴᴛ ꜱʟᴇᴇᴘɪɴɢ ᴘɪʟʟ": "https://radio.stereoscenic.com/asp-s",
        "ꜱᴜʙᴜʀʙᴀɴ ʟɪɢʜᴛꜱ": "https://ice1.somafm.com/suburbanlulls-128-mp3",
        "ᴀᴍʙɪᴇɴᴛ ꜰᴍ": "https://streams.fluxfm.de/ambient/mp3-128",
        "ɴᴀᴛᴜʀᴇ ꜱᴏᴜɴᴅꜱ": "https://streams.fluxfm.de/ambient/mp3-128",
    },
    "🌍 ɪɴᴛᴇʀɴᴀᴛɪᴏɴᴀʟ ʀᴀᴅɪᴏ": {
        "ᴅᴇᴇᴘ ʜᴏᴜꜱᴇ ᴍᴜꜱɪᴄ": "http://live.dancemusic.ro:7000/",
        "ʙᴀꜱᴇ ᴍᴜꜱɪᴄ": "https://base-music.stream.laut.fm/base-music",
        "ᴘᴜʟꜱᴇ ᴇᴅᴍ": "https://naxos.cdnstream.com/1373_128",
        "ʙᴇᴀᴛ ʙʟᴇɴᴅᴇʀ": "https://ice1.somafm.com/beatblender-128-mp3",
        "ᴇʟᴇᴄᴛʀᴏ ꜱᴡɪɴɢ": "https://ice1.somafm.com/seventies-128-mp3",
        "ɪɴᴅɪᴇ ᴘᴏᴘ": "https://ice1.somafm.com/indiepop-128-mp3",
    }
}


async def _safe_edit_caption(message, caption, reply_markup=None):
    try:
        await message.edit_caption(caption, reply_markup=reply_markup)
    except errors.FloodWait as fw:
        await asyncio.sleep(fw.value + 1)
        try:
            await message.edit_caption(caption, reply_markup=reply_markup)
        except Exception:
            pass
    except Exception:
        # Ignore MessageNotModified and other non-critical edit failures
        pass


def category_buttons():
    buttons_list = []
    category_list = list(RADIO_CATEGORIES.keys())
    for idx, category in enumerate(category_list):
        buttons_list.append([InlineKeyboardButton(
            category, callback_data=f"cat_{idx}")])

    buttons_list.append([InlineKeyboardButton(
        "ℹ️ ʜᴇʟᴘ", callback_data="radio_help_main")])

    return InlineKeyboardMarkup(buttons_list)


def radio_buttons(cat_idx, page=0, per_page=10):
    category_list = list(RADIO_CATEGORIES.keys())
    category = category_list[cat_idx]
    stations = sorted(RADIO_CATEGORIES[category].keys())
    total_pages = (len(stations) - 1) // per_page + 1
    start = page * per_page
    end = start + per_page
    current_stations = stations[start:end]

    # Create buttons in rows of 2
    buttons_list = []
    for i in range(0, len(current_stations), 2):
        row = []
        # Add first button in the row
        station_idx = stations.index(current_stations[i])
        row.append(InlineKeyboardButton(
            current_stations[i], callback_data=f"st_{cat_idx}_{station_idx}"))
        # Add second button if it exists
        if i + 1 < len(current_stations):
            station_idx = stations.index(current_stations[i + 1])
            row.append(InlineKeyboardButton(
                current_stations[i + 1], callback_data=f"st_{cat_idx}_{station_idx}"))
        buttons_list.append(row)

    # Navigation buttons
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(
            "◀️ ᴘʀᴇᴠ", callback_data=f"cp_{cat_idx}_{page-1}"))
    nav_buttons.append(InlineKeyboardButton(
        f"{page+1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(
            "▶️ ɴᴇxᴛ", callback_data=f"cp_{cat_idx}_{page+1}"))

    if nav_buttons:
        buttons_list.append(nav_buttons)

    # Back to categories button
    buttons_list.append([InlineKeyboardButton(
        "🔙 ʙᴀᴄᴋ", callback_data="back_to_categories")])

    return InlineKeyboardMarkup(buttons_list)


async def has_radio_control_permission(chat_id, user_id):
    # Check if anonymous admin
    if user_id == 1087968824:
        return True

    # Check if bot owner
    if user_id == config.OWNER_ID:
        return True

    # Check if sudo user
    if user_id in app.sudoers:
        return True

    # Check if authorized user in this chat
    if await db.is_auth(chat_id, user_id):
        return True

    # Check if chat admin
    try:
        member = await app.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except:
        return False


async def update_timer(chat_id, message_id, station_name, start_time):
    last_timer = None
    update_count = 0
    while True:
        try:
            # Check if call is still active - if not, stop updating
            if not await db.get_call(chat_id):
                LOGGER.debug(f"Radio timer stopped for {chat_id} - call ended")
                break

            elapsed = int(time.time() - start_time)
            mins, secs = divmod(elapsed, 60)
            timer = f"{mins:02d}:{secs:02d}"

            # Only update every 5 seconds to reduce API calls and lag
            if timer != last_timer and update_count % 5 == 0:
                try:
                    await app.edit_message_caption(
                        chat_id=chat_id,
                        message_id=message_id,
                        caption=f"📻 ɴᴏᴡ ᴘʟᴀʏɪɴɢ: {station_name}\n⏱️ ᴛɪᴍᴇ: {timer}",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton(
                                f"🎵 {station_name}", callback_data="noop")],
                            [
                                InlineKeyboardButton(
                                    "🔀 ꜱᴛᴀᴛɪᴏɴꜱ", callback_data="skip_radio"),
                                InlineKeyboardButton(
                                    "❌ ᴄʟᴏꜱᴇ", callback_data="close_message")
                            ]
                        ])
                    )
                    last_timer = timer
                except errors.FloodWait as fw:
                    # If rate limited, wait and continue without updating
                    await asyncio.sleep(fw.value)
                except Exception:
                    # Skip this update if any error
                    pass

            update_count += 1
        except Exception as e:
            # Silently ignore MESSAGE_NOT_MODIFIED, message deleted, or chat ended errors
            error_str = str(e)
            if not any(err in error_str for err in ["MESSAGE_NOT_MODIFIED", "MESSAGE_DELETE", "MESSAGE_ID_INVALID", "CHAT_ADMIN_REQUIRED"]):
                LOGGER.debug(f"Timer update error: {e}")
            break
        await asyncio.sleep(1)


@app.on_message(
    filters.command(["radio"])
    & filters.group
    & ~app.bl_users
)
@lang.language()
async def radio_handler(_, m: Message) -> None:
    # Auto-delete command message
    try:
        await m.delete()
    except Exception:
        pass

    await m.reply_text(
        "📻 ꜱᴇʟᴇᴄᴛ ᴀ ʀᴀᴅɪᴏ ᴄᴀᴛᴇɢᴏʀʏ:",
        reply_markup=category_buttons(),
    )


@app.on_callback_query(filters.regex(r"^cat_"))
async def on_category_select(_, callback_query):
    """Handle category selection."""
    await callback_query.answer()
    parts = callback_query.data.split("_")
    cat_idx = int(parts[1])
    category_list = list(RADIO_CATEGORIES.keys())
    category = category_list[cat_idx]

    try:
        await callback_query.message.edit_text(
            f"📻 {category}\n\nꜱᴇʟᴇᴄᴛ ᴀ ꜱᴛᴀᴛɪᴏɴ:",
            reply_markup=radio_buttons(cat_idx, page=0)
        )
    except errors.FloodWait as e:
        await asyncio.sleep(e.value)
        await callback_query.message.edit_text(
            f"📻 {category}\n\nꜱᴇʟᴇᴄᴛ ᴀ ꜱᴛᴀᴛɪᴏɴ:",
            reply_markup=radio_buttons(cat_idx, page=0)
        )
    except Exception:
        pass


@app.on_callback_query(filters.regex(r"^cp_"))
async def on_category_page_change(_, callback_query):
    """Handle pagination within a category."""
    await callback_query.answer()
    parts = callback_query.data.split("_")
    cat_idx = int(parts[1])
    page = int(parts[2])

    try:
        await callback_query.message.edit_reply_markup(radio_buttons(cat_idx, page=page))
    except errors.FloodWait as e:
        await asyncio.sleep(e.value)
        try:
            await callback_query.message.edit_reply_markup(radio_buttons(cat_idx, page=page))
        except errors.MessageNotModified:
            pass
    except errors.MessageNotModified:
        pass
    except Exception:
        pass


@app.on_callback_query(filters.regex(r"^back_to_categories"))
async def on_back_to_categories(_, callback_query):
    """Handle back to categories button."""
    await callback_query.answer()

    try:
        await callback_query.message.edit_text(
            "📻 ꜱᴇʟᴇᴄᴛ ᴀ ʀᴀᴅɪᴏ ᴄᴀᴛᴇɢᴏʀʏ:",
            reply_markup=category_buttons()
        )
    except errors.FloodWait as e:
        await asyncio.sleep(e.value)
        await callback_query.message.edit_text(
            "📻 ꜱᴇʟᴇᴄᴛ ᴀ ʀᴀᴅɪᴏ ᴄᴀᴛᴇɢᴏʀʏ:",
            reply_markup=category_buttons()
        )
    except Exception:
        pass


@app.on_callback_query(filters.regex(r"^st_"))
async def on_station_select(_, callback_query):
    """Handle station selection and start playback."""
    parts = callback_query.data.split(
        "_")  # Split into ['st', 'cat_idx', 'station_idx']
    cat_idx = int(parts[1])
    station_idx = int(parts[2])

    # Get actual category and station names
    category_list = list(RADIO_CATEGORIES.keys())
    category = category_list[cat_idx]
    stations = sorted(RADIO_CATEGORIES[category].keys())
    station_name = stations[station_idx]
    RADIO_URL = RADIO_CATEGORIES[category].get(station_name)

    if not RADIO_URL:
        return await callback_query.answer("❌ ɪɴᴠᴀʟɪᴅ ꜱᴛᴀᴛɪᴏɴ ɴᴀᴍᴇ.", show_alert=True)

    # Always get the group chat ID where the button was clicked
    group_chat_id = callback_query.message.chat.id

    # Check if this is a channel - if so, skip (buttons should only work in groups)
    try:
        chat_type = callback_query.message.chat.type
        if chat_type == enums.ChatType.CHANNEL:
            return await callback_query.answer("❌ ᴘʟᴇᴀꜱᴇ ᴜꜱᴇ ʀᴀᴅɪᴏ ᴄᴏᴍᴍᴀɴᴅ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ.", show_alert=True)
    except:
        pass

    # Always play radio in the group voice chat
    playback_chat_id = group_chat_id

    # Check if radio is already playing - only authorized users can switch
    if await db.get_call(playback_chat_id):
        # Check if user has permission
        if not await has_radio_control_permission(playback_chat_id, callback_query.from_user.id):
            return await callback_query.answer(
                "❌ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ, ʙᴏᴛ ᴏᴡɴᴇʀ, ꜱᴜᴅᴏ ᴜꜱᴇʀꜱ, ᴏʀ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜꜱᴇʀꜱ ᴄᴀɴ ᴄʜᴀɴɢᴇ ᴛʜᴇ ꜱᴛᴀᴛɪᴏɴ ᴡʜɪʟᴇ ʀᴀᴅɪᴏ ɪꜱ ᴘʟᴀʏɪɴɢ.\n"
                "ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ꜰᴏʀ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ꜱᴇꜱꜱɪᴏɴ ᴛᴏ ᴇɴᴅ.",
                show_alert=True
            )

    # If assistant is not in the group, invite them before playing
    if playback_chat_id not in db.active_calls:
        client = await db.get_client(playback_chat_id)
        try:
            member = await app.get_chat_member(playback_chat_id, client.id)
            if member.status in [
                enums.ChatMemberStatus.BANNED,
                enums.ChatMemberStatus.RESTRICTED,
            ]:
                try:
                    await app.unban_chat_member(chat_id=playback_chat_id, user_id=client.id)
                except:
                    return await callback_query.answer(
                        f"❌ ᴀꜱꜱɪꜱᴛᴀɴᴛ {client.mention} ɪꜱ ʙᴀɴɴᴇᴅ!\n"
                        f"ᴜɴʙᴀɴ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.",
                        show_alert=True
                    )
        except errors.ChatAdminRequired:
            return await callback_query.answer(
                "❌ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴛᴏ ɪɴᴠɪᴛᴇ ᴀꜱꜱɪꜱᴛᴀɴᴛ!",
                show_alert=True
            )
        except errors.UserNotParticipant:
            # Assistant not in group - invite them
            if callback_query.message.chat.username:
                invite_link = callback_query.message.chat.username
                try:
                    await client.resolve_peer(invite_link)
                except:
                    pass
            else:
                try:
                    invite_link = (await app.get_chat(playback_chat_id)).invite_link
                    if not invite_link:
                        invite_link = await app.export_chat_invite_link(playback_chat_id)
                except errors.ChatAdminRequired:
                    return await callback_query.answer(
                        "❌ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴛᴏ ɪɴᴠɪᴛᴇ ᴀꜱꜱɪꜱᴛᴀɴᴛ!",
                        show_alert=True
                    )
                except Exception as ex:
                    return await callback_query.answer(
                        f"❌ ᴇʀʀᴏʀ: {type(ex).__name__}",
                        show_alert=True
                    )

            await callback_query.answer("🔄 ɪɴᴠɪᴛɪɴɢ ᴀꜱꜱɪꜱᴛᴀɴᴛ...")
            await asyncio.sleep(1)

            try:
                await client.join_chat(invite_link)
            except errors.UserAlreadyParticipant:
                pass
            except errors.InviteRequestSent:
                try:
                    await app.approve_chat_join_request(playback_chat_id, client.id)
                except Exception as ex:
                    return await callback_query.answer(
                        f"❌ ᴇʀʀᴏʀ: {type(ex).__name__}",
                        show_alert=True
                    )
            except Exception as ex:
                return await callback_query.answer(
                    f"❌ ᴇʀʀᴏʀ: {type(ex).__name__}",
                    show_alert=True
                )

            await client.resolve_peer(playback_chat_id)

    # Answer callback immediately to prevent lag
    await callback_query.answer()

    mention = callback_query.from_user.mention if callback_query.from_user.id != 1087968824 else "ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ"

    # Keep the station selection message visible - don't delete it
    # Users can continue selecting stations from the same button list

    # IMPORTANT: Always send thumbnail to the group where the command was issued
    # Even if channel play is enabled, the control panel should be in the group, not the channel

    # Send processing message to the group where the command was issued
    try:
        mystic = await app.send_message(
            chat_id=group_chat_id,
            text=f"<blockquote>📻 ᴘʀᴏᴄᴇꜱꜱɪɴɢ {station_name}...</blockquote>"
        )
    except errors.FloodWait as e:
        await asyncio.sleep(e.value)
        mystic = await app.send_message(
            chat_id=group_chat_id,
            text=f"<blockquote>📻 ᴘʀᴏᴄᴇꜱꜱɪɴɢ {station_name}...</blockquote>"
        )

    start_time = time.time()
    asyncio.create_task(update_timer(
        group_chat_id, mystic.id, station_name, start_time))

    # Create a file object for radio stream
    class RadioFile:
        def __init__(self, url, title):
            self.url = url
            self.title = title
            self.is_live = True
            self.duration = "ʟɪᴠᴇ ꜱᴛʀᴇᴀᴍ"
            self.duration_sec = 0
            self.file_path = url  # Use URL as file path for streaming
            self.id = url
            self.message_id = mystic.id
            self.user = mention
            self.thumb = config.RADIO_IMG
            self.video = False  # Audio only for radio

    file = RadioFile(RADIO_URL, f"📻 {station_name}")

    # Check if already playing - switch to new station immediately
    if await db.get_call(playback_chat_id):
        # Clear queue and stop current playback
        queue.clear(playback_chat_id)
        try:
            await tune.stop_stream(playback_chat_id)
        except:
            pass

    # Add new station to queue
    position = queue.add(playback_chat_id, file)

    # Play the stream (use playback_chat_id for actual audio)
    try:
        await tune.play_media(
            chat_id=playback_chat_id,
            message=mystic,
            media=file,
        )
    except errors.FloodWait as fw:
        # Back off then retry once to avoid cascading FLOOD_WAIT
        await asyncio.sleep(fw.value + 1)
        try:
            await tune.play_media(
                chat_id=playback_chat_id,
                message=mystic,
                media=file,
            )
        except Exception as retry_err:
            await _safe_edit_caption(
                mystic,
                f"❌ ᴇʀʀᴏʀ ᴘʟᴀʏɪɴɢ ʀᴀᴅɪᴏ:\n{retry_err}"
            )
            LOGGER.error(f"Radio play retry failed: {retry_err}")
            queue.clear(playback_chat_id)
            await db.remove_call(playback_chat_id)
    except Exception as e:
        await _safe_edit_caption(
            mystic,
            f"❌ ᴇʀʀᴏʀ ᴘʟᴀʏɪɴɢ ʀᴀᴅɪᴏ:\n{e}"
        )
        LOGGER.error(f"Radio play error: {e}")
        queue.clear(playback_chat_id)
        await db.remove_call(playback_chat_id)


@app.on_callback_query(filters.regex(r"^skip_radio"))
async def skip_radio_callback(_, callback_query):
    """Handle skip radio button - show station list."""
    # Anyone can browse stations, not just admins
    await callback_query.answer()

    # Determine the correct chat to send message to
    callback_chat_id = callback_query.message.chat.id
    callback_chat_type = callback_query.message.chat.type

    # If callback came from a channel, find the linked group
    if callback_chat_type == enums.ChatType.CHANNEL:
        # This is a channel - we need to send to the group instead
        # For now, just answer and don't allow action from channel
        return await callback_query.answer(
            "⚠️ ᴘʟᴇᴀꜱᴇ ᴜꜱᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴꜱ ꜰʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ ᴄʜᴀᴛ, ɴᴏᴛ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ.",
            show_alert=True
        )

    try:
        await callback_query.message.reply_text(
            "📻 ꜱᴇʟᴇᴄᴛ ᴀ ʀᴀᴅɪᴏ ᴄᴀᴛᴇɢᴏʀʏ:",
            reply_markup=category_buttons()
        )
    except errors.FloodWait as e:
        await asyncio.sleep(e.value)
        await callback_query.message.reply_text(
            "📻 ꜱᴇʟᴇᴄᴛ ᴀ ʀᴀᴅɪᴏ ᴄᴀᴛᴇɢᴏʀʏ:",
            reply_markup=category_buttons()
        )
    except Exception:
        pass


@app.on_callback_query(filters.regex(r"^close_message"))
async def close_message_callback(_, callback_query):
    """Handle close button."""
    try:
        # Check if user has permission to delete
        if await has_radio_control_permission(callback_query.message.chat.id, callback_query.from_user.id):
            await callback_query.message.delete()
            await callback_query.answer()
        else:
            await callback_query.answer(
                "❌ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ, ʙᴏᴛ ᴏᴡɴᴇʀ, ꜱᴜᴅᴏ ᴜꜱᴇʀꜱ, ᴏʀ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜꜱᴇʀꜱ ᴄᴀɴ ᴄʟᴏꜱᴇ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ.",
                show_alert=True
            )
    except Exception as e:
        await callback_query.answer(f"❌ ᴇʀʀᴏʀ: {str(e)}", show_alert=True)


@app.on_callback_query(filters.regex(r"^radio_help_"))
async def on_radio_help(_, callback_query):

    help_text = (
        "<blockquote>📻 ʀᴀᴅɪᴏ ᴘʟᴜɢɪɴ ʜᴇʟᴘ</blockquote>\n\n"
        "<blockquote>• ᴛʏᴘᴇ `/radio` ᴛᴏ ᴏᴘᴇɴ ᴄᴀᴛᴇɢᴏʀʏ ʟɪꜱᴛ\n"
        "• ꜱᴇʟᴇᴄᴛ ᴀ ᴄᴀᴛᴇɢᴏʀʏ ᴛᴏ ʙʀᴏᴡꜱᴇ ꜱᴛᴀᴛɪᴏɴꜱ\n"
        "• ᴜꜱᴇ `/stop` ᴛᴏ ꜱᴛᴏᴘ ᴘʟᴀʏʙᴀᴄᴋ</blockquote>"
    )

    await callback_query.message.edit_text(
        help_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 ʙᴀᴄᴋ ᴛᴏ ᴄᴀᴛᴇɢᴏʀɪᴇꜱ",
                                  callback_data="back_to_categories")]
        ])
    )


@app.on_callback_query(filters.regex(r"^noop"))
async def on_noop(_, callback_query):
    """Handle no-operation button."""
    await callback_query.answer("🎵 ᴇɴᴊᴏʏɪɴɢ ᴛʜᴇ ᴍᴜꜱɪᴄ!", show_alert=False)