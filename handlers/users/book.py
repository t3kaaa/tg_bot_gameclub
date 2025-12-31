from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto,Message
from utils.services.api import fetch_zones,fetch_devices,fetch_rooms,book_device_api,fetch_device_detail,book_room_api, fetch_room_detail
from utils.text import zone_caption,device_caption
from keyboards.inline.buttons import zone_kb,rooms_kb,devices_kb,hours_kb,are_you_sure,admin_booking_kb,back_to_main
from loader import db
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from utils.language import t
from states.test import BookingState
from datetime import datetime,timezone,timedelta
from data.config import ADMINS
from django.utils import timezone
from zoneinfo import ZoneInfo

tz = ZoneInfo("Asia/Tashkent")
router = Router()

#___________________________________________________________ With Zone  ______________________________________________________________ 
@router.callback_query(F.data == "booking")
async def booking_start(call: CallbackQuery):
    photo = FSInputFile('media/zone/comfort_zone.jpg')
    telegram_id = call.from_user.id
    token = await db.get_token(telegram_id)
    lang = await db.get_language(telegram_id)
	
    data = await fetch_zones(token["access"], telegram_id, page=1)
    zone = data["results"][0]

    await call.message.edit_media(
        InputMediaPhoto(
            media=photo,
            caption=zone_caption(zone, lang)
        ),
        reply_markup= await zone_kb(
            telegram_id=telegram_id,
            page=1,
            has_next=data["next"] is not None,
            has_prev=False,
            zone_id=zone["id"]
        )
    )
    
@router.callback_query(F.data.startswith("zone_page_"))
async def zone_pagination(call: CallbackQuery):
    telegram_id = call.from_user.id
    page = int(call.data.split("_")[-1])

    token = await db.get_token(telegram_id)
    lang = await db.get_language(telegram_id)

    data = await fetch_zones(token["access"], telegram_id, page)
    zone = data["results"][0]

    await call.message.edit_caption(caption=zone_caption(zone, lang),reply_markup= await zone_kb(
			telegram_id=telegram_id,
			page=page,
			has_next=data["next"] is not None,
			has_prev=data["previous"] is not None,
			zone_id=zone["id"]
		))
       




#___________________________________________________________ With Room ______________________________________________________________           

@router.callback_query(F.data.startswith("zone_rooms_"))
async def open_rooms(call: CallbackQuery):
    telegram_id = call.from_user.id
    zone_id = int(call.data.split("_")[-1])

    token = await db.get_token(telegram_id)
    data = await fetch_rooms(token["access"], telegram_id, zone_id, page=1)

    if not data["results"]:
        await call.answer("No rooms", show_alert=True)
        return

    room = data["results"][0]

    text = (
        f"{await t(telegram_id, 'rooms_title')}\n\n"
        f"🛋 <b>{room['name']}</b>\n"
        f"{room.get('description', '')}"
    )

    photo = FSInputFile("media/room/room1_comfort.jpg")

    await call.message.edit_media(
        InputMediaPhoto(media=photo, caption=text),
        reply_markup=await rooms_kb(
            telegram_id=telegram_id,
            zone_id=zone_id,
            room_id=room["id"],
            page=1,
            has_next=data["next"] is not None,
            has_prev=False,
        ),
    )
    
@router.callback_query(F.data.startswith("rooms_"))
async def rooms_pagination(call: CallbackQuery):
    _, zone_id, page = call.data.split("_")
    zone_id = int(zone_id)
    page = int(page)

    telegram_id = call.from_user.id
    token = await db.get_token(telegram_id)

    data = await fetch_rooms(token["access"], telegram_id, zone_id, page=page)

    if not data["results"]:
        await call.answer("No rooms", show_alert=True)
        return

    room = data["results"][0]

    text = (
        f"{await t(telegram_id, 'rooms_title')}\n\n"
        f"🛋 <b>{room['name']}</b>\n"
        f"{room.get('description', '')}"
    )

    await call.message.edit_caption(
        caption=text,
        reply_markup=await rooms_kb(
            telegram_id=telegram_id,
            zone_id=zone_id,
            room_id=room["id"],
            page=page,
            has_next=data["next"] is not None,
            has_prev=data["previous"] is not None,
        ),
    )

@router.callback_query(F.data.startswith("book_room_"))
async def book_room_start(call: CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    room_id = int(call.data.split("_")[-1])

    token = (await db.get_token(telegram_id))["access"]

    try:
        room = await fetch_room_detail(token, telegram_id, room_id)
    except Exception:
        await call.answer("Room not found", show_alert=True)
        return

    await state.update_data(
        room_id=room_id,
        zone_id=room["zone_id"],
    )

    await state.set_state(BookingState.choose_time)

    await call.message.answer(
        await t(telegram_id, "booking_enter_time")
    )



@router.message(BookingState.choose_time)
async def receive_time(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    text = message.text.strip()

    try:
        time_obj = datetime.strptime(text, "%H:%M").time()
    except ValueError:
        await message.answer(
            await t(telegram_id, "booking_time_format_error")
        )
        return

    now = datetime.now(tz)
    start_time = datetime.combine(now.date(), time_obj, tzinfo=tz)

    if start_time <= now:
        await message.answer(
            await t(
                telegram_id,
                "booking_time_past_error",
                now=now.strftime("%H:%M"),
            )
        )
        return

    await state.update_data(start_time=start_time)
    await state.set_state(BookingState.choose_hours)

    await message.answer(
        await t(telegram_id, "booking_choose_hours"),
        reply_markup=await hours_kb(telegram_id),
    )


@router.callback_query(
    BookingState.choose_hours,
    F.data.startswith("hours_pick_"),
)
async def choose_hours(call: CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    hours = int(call.data.replace("hours_pick_", ""))

    data = await state.get_data()
    start_time = data["start_time"]
    end_time = start_time + timedelta(hours=hours)

    await state.update_data(end_time=end_time)
    await state.set_state(BookingState.confirm)

    await call.message.answer(
        await t(
            telegram_id,
            "booking_confirm_title",
            start=start_time.strftime("%H:%M"),
            hours=hours,
        ),
        reply_markup=await are_you_sure(telegram_id),
    )

@router.callback_query(BookingState.choose_hours, F.data.startswith("hours_page_"))
async def hours_pagination(call: CallbackQuery):
    telegram_id = call.from_user.id
    page = int(call.data.split("_")[-1])

    await call.message.edit_reply_markup(
        reply_markup=await hours_kb(telegram_id=telegram_id, page=page)
    )



@router.callback_query(F.data == "ha", BookingState.confirm)
async def confirm_room_booking(call: CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    data = await state.get_data()

    token = (await db.get_token(telegram_id))["access"]
    lang = await db.get_language(telegram_id)

    payload = {
        "zone": data["zone_id"],
        "room": data["room_id"],
        "start_time": data["start_time"].isoformat(),
        "end_time": data["end_time"].isoformat(),
    }

    result = await book_room_api(
        access_token=token,
        lang=lang,
        payload=payload,
    )

    if not result.get("ok"):
        error = result.get("data") or result.get("error")

        if isinstance(error, dict):
            if "non_field_errors" in error:
                error = error["non_field_errors"][0]
            else:
                error = next(iter(error.values()))[0]

        await call.message.answer(
            f"❌ {error}",
            reply_markup=await back_to_main(telegram_id),
        )
        return

    booking = result["data"]
    booking_id = booking.get("id")

    await call.message.answer(
        await t(telegram_id, "booking_confirmed_sent"),
        reply_markup=await back_to_main(telegram_id),
    )

    await state.clear()

    username = call.from_user.username or call.from_user.full_name
    admin_text = (
        "📥 <b>NEW ROOM BOOKING</b>\n\n"
        f"👤 User: {username}\n"
        f"🆔 Booking ID: {booking_id}\n"
        f"🛋 Room ID: {data['room_id']}\n"
        f"⏰ {data['start_time'].strftime('%H:%M')} → {data['end_time'].strftime('%H:%M')}"
    )

    for admin_id in ADMINS:
        await call.bot.send_message(
            chat_id=admin_id,
            text=admin_text,
            reply_markup=await admin_booking_kb(
                booking_id=booking_id,
                telegram_id=telegram_id,
            ),
        )

@router.callback_query(F.data == "yoq", BookingState.confirm)
async def cancel_room_booking(call: CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    await state.clear()

    await call.message.answer(
        await t(telegram_id, "booking_cancelled"),
        reply_markup=await back_to_main(telegram_id),
    )
#___________________________________________________________ With Device ________________________________________________________________________________________

@router.callback_query(F.data.startswith("zone_devices_"))
async def open_devices(call: CallbackQuery):
    telegram_id = call.from_user.id
    zone_id = int(call.data.split("_")[-1])

    token = await db.get_token(telegram_id)
    data = await fetch_devices(token["access"],telegram_id,zone_id,page=1)

    if not data["results"]:
        await call.answer("No devices", show_alert=True)
        return

    device = data["results"][0]


    await call.message.edit_caption(
        caption=await device_caption(device, telegram_id),
        reply_markup=await devices_kb(
            telegram_id=telegram_id,
            zone_id=zone_id,
            page=1,
            has_next=data["next"] is not None,
            has_prev=False,
            device_id=device["id"]
        )
    )
    
@router.callback_query(F.data.startswith("devices_"))
async def devices_pagination(call: CallbackQuery):
    _, zone_id, page = call.data.split("_")
    zone_id = int(zone_id)
    page = int(page)

    telegram_id = call.from_user.id
    token = await db.get_token(telegram_id)

    data = await fetch_devices(
        token["access"],
        telegram_id,
        zone_id,
        page=page
    )

    if not data["results"]:
        await call.answer("No devices", show_alert=True)
        return

    device = data["results"][0]
    print()

    await call.message.edit_caption(
        caption=await device_caption(device, telegram_id),
        reply_markup=await devices_kb(
            telegram_id=telegram_id,
            zone_id=zone_id,
            page=page,
            has_next=data["next"] is not None,
            has_prev=data["previous"] is not None,
            device_id=device["id"]
        )
    )


@router.callback_query(F.data.startswith("book_device_"))
async def book_device_start(call: CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    device_id = int(call.data.split("_")[-1])

    token = (await db.get_token(telegram_id))["access"]
    device = await fetch_device_detail(token, telegram_id, device_id)

    await state.update_data(
        device_id=device_id,
        zone_id=device["zone_id"]
    )

    await state.set_state(BookingState.choose_time)

    await call.message.answer(
        await t(telegram_id, "booking_enter_time")
    )



@router.message(BookingState.choose_time)
async def receive_time(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    text = message.text.strip()

    try:
        time_obj = datetime.strptime(text, "%H:%M").time()
    except ValueError:
        await message.answer(
            await t(telegram_id, "booking_time_format_error")
        )
        return

   
    

    now = datetime.now(tz)
    start_time = datetime.combine(now.date(),time_obj,tzinfo=tz)

    if start_time <= now:
        await message.answer(
            await t(
                telegram_id,
                "booking_time_past_error",
                now=now.strftime("%H:%M")
            )
        )
        return

    await state.update_data(start_time=start_time)
    await state.set_state(BookingState.choose_hours)

    await message.answer(
        await t(telegram_id, "booking_choose_hours"),
        reply_markup=await hours_kb(telegram_id)
    )


@router.callback_query(BookingState.choose_hours, F.data.startswith("hours_pick_"))
async def choose_hours(call: CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    hours = int(call.data.replace("hours_pick_", ""))

    data = await state.get_data()
    start_time = data["start_time"]
    print(start_time)
    end_time = start_time + timedelta(hours=hours)

    await state.update_data(end_time=end_time)
    await state.set_state(BookingState.confirm)

    await call.message.answer(
        await t(
            telegram_id,
            "booking_confirm_title",
            start=start_time.strftime("%H:%M"),
            hours=hours
        ),
        reply_markup=await are_you_sure(telegram_id)
    )


@router.callback_query(BookingState.choose_hours, F.data.startswith("hours_page_"))
async def hours_pagination(call: CallbackQuery):
    telegram_id = call.from_user.id
    page = int(call.data.split("_")[-1])

    await call.message.edit_reply_markup(
        reply_markup=await hours_kb(telegram_id=telegram_id, page=page)
    )

@router.callback_query(F.data == "ha")
async def confirm_booking(call: CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    data = await state.get_data()

    token = (await db.get_token(telegram_id))["access"]
    lang = await db.get_language(telegram_id)

    start_time = data.get("start_time")
    start_time = start_time.isoformat()
   
   
    
    end_time = data.get("end_time")
    end_time = end_time.isoformat()
    
    payload = {
        "zone": data["zone_id"],
        "device": data["device_id"],
        "start_time": start_time,
        "end_time": end_time,
    }

    result = await book_device_api(access_token=token, lang=lang, payload=payload)

    if not result.get("ok"):
        await call.message.answer(
            await t(telegram_id, "booking_error"),
            reply_markup=await back_to_main(telegram_id)
        )
        return

    resp = result["data"]
    booking_id = resp.get("id") or resp.get("booking_id")

    

    await call.message.answer(
        await t(telegram_id, "booking_confirmed_sent"),
        reply_markup=await back_to_main(telegram_id)
    )

    await state.clear()

    username = call.from_user.username or call.from_user.full_name
    admin_text = (
        "📥 <b>NEW BOOKING</b>\n\n"
        f"👤 User: {username}\n"
        f"🆔 Booking ID: {booking_id}\n"
        f"🖥 Device ID: {data['device_id']}\n"
        f"⏰ {data['start_time'].strftime('%H:%M')} → {data['end_time'].strftime('%H:%M')}"
    )

    for admin_id in ADMINS:
        await call.bot.send_message(
            chat_id=admin_id,
            text=admin_text,
            reply_markup=await admin_booking_kb(booking_id=booking_id,telegram_id=telegram_id)
        )

@router.callback_query(F.data == "yoq", BookingState.confirm)
async def cancel_booking(call: CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id

    await state.clear()

    await call.message.answer(
        await t(telegram_id, "booking_cancelled"),
        reply_markup=await back_to_main(telegram_id)
    )

import httpx

@router.callback_query(F.data.startswith("admin_booking_missed_"))
async def admin_booking_missed(call: CallbackQuery):
    booking_id = int(call.data.split("_")[-1])
    token = (await db.get_admin_token())
    lang = await db.get_language(telegram_id=call.message.from_user.id)

    async with httpx.AsyncClient() as client:
        await client.patch(
            f"http://127.0.0.1:8000/{lang}/api/admin/booking/{booking_id}/",
            headers={"Authorization": f"Bearer {token}"},
            json={"status": "missed"}
        )

    await call.message.edit_text("❌ Booking MISSED qilindi")


@router.callback_query(F.data.startswith("admin_booking_active_"))
async def admin_booking_active(call: CallbackQuery):
    raw_id = call.data.split("_")[-1]

    if raw_id == "None":
        await call.answer("❌ Booking ID yo‘q", show_alert=True)
        return

    booking_id = int(raw_id)

    token = await db.get_admin_token()
    lang = await db.get_language(call.from_user.id)

    async with httpx.AsyncClient() as client:
        await client.patch(
            f"http://127.0.0.1:8000/{lang}/api/admin/booking/{booking_id}/",
            headers={"Authorization": f"Bearer {token}"},
            json={"status": "active"},
        )

    await call.message.edit_text("✅ Booking ACTIVE qilindi")