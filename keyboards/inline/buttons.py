from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loader import db
from utils.language import t

select_language = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="🇺🇿 Uz", callback_data='uz'),
        InlineKeyboardButton(text="🇷🇺 Ru", callback_data='ru'),
        InlineKeyboardButton(text="🇬🇧 En", callback_data='en')
    ]]
)



async def back_to_main(telegram_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=await t(telegram_id, 'back_btn'), callback_data="main")]
        ]
    )



async def kb(telegram_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=await t(telegram_id, 'login_btn'), callback_data="login"),
                InlineKeyboardButton(text=await t(telegram_id, 'register_btn'), callback_data="register")
            ]
        ]
    )

async def main_kb(telegram_id):
    lang = await db.get_language(telegram_id)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=await t(telegram_id, 'account_btn'), callback_data="account"),
                InlineKeyboardButton(text=await t(telegram_id, 'booking_btn'), callback_data="booking")
            ],
            [
                InlineKeyboardButton(text=await t(telegram_id, 'history_btn'), callback_data="history"),
                InlineKeyboardButton(text=await t(telegram_id, 'web_site_btn'), url="http://127.0.0.1:8000")
            ]
        ]
    )

async def are_you_sure(telegram_id):
    lang = await db.get_language(telegram_id)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=await t(telegram_id, 'yes_btn'), callback_data='ha'),
                InlineKeyboardButton(text=await t(telegram_id, 'no_btn'), callback_data='yoq')
            ]
        ]
    )

async def account_kb(telegram_id):
    lang = await db.get_language(telegram_id)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=await t(telegram_id, 'logout_btn'), callback_data="logout"),
                InlineKeyboardButton(text=await t(telegram_id, 'back_btn'), callback_data="main")
            ]
        ]
    )


async def history_kb(telegram_id: int,page: int, has_next: bool, has_prev: bool):
    kb = InlineKeyboardMarkup(inline_keyboard=[])

    nav = []
    if has_prev:
        nav.append(
            InlineKeyboardButton(text="⬅️", callback_data=f"history_page_{page-1}")
        )
    if has_next:
        nav.append(
            InlineKeyboardButton(text="➡️", callback_data=f"history_page_{page+1}")
        )

    if nav:
        kb.inline_keyboard.append(nav)

    kb.inline_keyboard.append(
        [InlineKeyboardButton(text=await t(telegram_id, 'back_btn'), callback_data="main")]
    )

    return kb

async def zone_kb(telegram_id: int,page: int,has_next: bool,has_prev: bool,zone_id: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[])

    nav = []
    if has_prev:
        nav.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"zone_page_{page-1}"
            )
        )
    if has_next:
        nav.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"zone_page_{page+1}"
            )
        )

    if nav:
        kb.inline_keyboard.append(nav)

    kb.inline_keyboard.append([
        InlineKeyboardButton(text=await t(telegram_id, "rooms_btn", default_text="🛋 Rooms"),callback_data=f"zone_rooms_{zone_id}"),
        InlineKeyboardButton(text=await t(telegram_id, "devices_btn", default_text="🖥 Devices"),callback_data=f"zone_devices_{zone_id}"),
    ])


    kb.inline_keyboard.append([InlineKeyboardButton(text=await t(telegram_id, "back_btn"),callback_data="main")])

    return kb

async def rooms_kb(
    telegram_id: int,
    zone_id: int,
    room_id: int,
    page: int,
    has_next: bool,
    has_prev: bool,
):
    kb = InlineKeyboardMarkup(inline_keyboard=[])

    nav = []
    if has_prev:
        nav.append(
            InlineKeyboardButton(
                text="⬅️", callback_data=f"rooms_{zone_id}_{page-1}"
            )
        )
    if has_next:
        nav.append(
            InlineKeyboardButton(
                text="➡️", callback_data=f"rooms_{zone_id}_{page+1}"
            )
        )
    if nav:
        kb.inline_keyboard.append(nav)

    kb.inline_keyboard.append(
        [
            InlineKeyboardButton(
                text=await t(telegram_id, "book_btn"),
                callback_data=f"book_room_{room_id}",
            )
        ]
    )

    kb.inline_keyboard.append(
        [
            InlineKeyboardButton(
                text=await t(telegram_id, "back_btn"),
                callback_data="booking",
            )
        ]
    )

    return kb
async def devices_kb(telegram_id: int,zone_id: int,page: int,has_next: bool,has_prev: bool,device_id: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[])

    nav = []
    if has_prev:
        nav.append(
            InlineKeyboardButton(text="⬅️", callback_data=f"devices_{zone_id}_{page-1}")
        )
    if has_next:
        nav.append(
            InlineKeyboardButton(text="➡️", callback_data=f"devices_{zone_id}_{page+1}")
        )
    if nav:
        kb.inline_keyboard.append(nav)

    kb.inline_keyboard.append([InlineKeyboardButton(text=await t(telegram_id, "book_btn"),callback_data=f"book_device_{device_id}")])

    kb.inline_keyboard.append([InlineKeyboardButton(text=await t(telegram_id, "back_btn"),callback_data=f"booking")])

    return kb



async def hours_kb(telegram_id: int, page: int = 1):
    kb = InlineKeyboardMarkup(inline_keyboard=[])

    hours = range(1, 7) if page == 1 else range(7, 13)

    row = []
    for h in hours:
        row.append(
            InlineKeyboardButton(
                text=f"{h} ⏱",
                callback_data=f"hours_pick_{h}"
            )
        )
        if len(row) == 3:
            kb.inline_keyboard.append(row)
            row = []
    if row:
        kb.inline_keyboard.append(row)

    nav = []
    if page == 2:
        nav.append(InlineKeyboardButton(text="⬅️", callback_data="hours_page_1"))
    if page == 1:
        nav.append(InlineKeyboardButton(text="➡️", callback_data="hours_page_2"))
    if nav:
        kb.inline_keyboard.append(nav)

    kb.inline_keyboard.append([
        InlineKeyboardButton(text=await t(telegram_id, "back_btn"), callback_data="back_time")
    ])
    return kb

async def admin_booking_kb(booking_id: int,telegram_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=await t(telegram_id=telegram_id, key='active_cfrm_btn'),
                    callback_data=f"admin_booking_active_{booking_id}"
                ),
                InlineKeyboardButton(
                    text=await t(telegram_id=telegram_id, key='missed_cfrm_btn'),
                    callback_data=f"admin_booking_missed_{booking_id}"
                )
            ]
        ]
    )