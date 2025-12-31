from .language import t

def history_text(items: list) -> str:
    if not items:
        return "📭 Bookinglar yo‘q"

    text = "📜 <b>Booking history</b>\n\n"

    for i in items:
        device = i.get("device")
        zone = i.get("zone")

        if isinstance(device, dict):
            device_text = device.get("type", "—").upper()
        else:
            device_text = f"ID {device}"

        if isinstance(zone, dict):
            zone_text = zone.get("name", "—")
        else:
            zone_text = f"ID {zone}"

        text += (
            f"🎮 <b>{device_text}</b> | {zone_text}\n"
            f"⏰ {i['start_time']} → {i['end_time']}\n"
            f"📌 {i['status'].upper()}\n\n"
        )

    return text


def zone_caption(zone, lang: str):
    if lang == "ru":
        return (
            f"🎮 <b>Это  {zone['name']} зона </b>\n\n"
            f"❕ В данный момент у нас более 100 устройств, и часть из них находится здесь.\n"
            f"💰 Цена: {zone['total_price']} сум"
        )
    if lang == "en":
        return (
            f"🎮 <b>This is {zone['name']} zone </b>\n\n"
            f"❕ Right now. We have more 100 devices and part of them are there\n"
            f"💰 Price: {zone['total_price']} sum"
        )
    return (
        f"🎮 <b>Bu shu zona {zone['name']}</b>\n\n"
        f"❕ Hozirda bizda 100 dan ortiq qurilmalar mavjud va ularning bir qismi hozir shu yerda joylashgan.\n"
        f"💰 Narx: {zone['total_price']} so‘m"
    )

async def device_caption(device: dict, telegram_id: int) -> str:
    status = device.get("status")
    print(status)          
    is_booked = device.get("is_booked")    

    if is_booked == False:
        status_icon = "🟡"
        status_text = await t(telegram_id, "device_status_pending")

    if is_booked == True:
        status_icon = "🔴"
        status_text = await t(telegram_id, "device_status_busy")



    description = device.get("description") or "-"
    monitor = device.get("screen") or "-"

    return (
        f"{await t(telegram_id, 'devices_title')}\n\n"
        f"🖥 <b>{device['type'].upper()}</b>\n"
        f"🖥 Monitor: {monitor}\n"
        f"📝 {description}\n\n"
        f"{status_icon} {status_text}"
    )