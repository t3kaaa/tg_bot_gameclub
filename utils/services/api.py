import httpx
from loader import db 



async def fetch_history(telegram_id: int, access_token: str, page: int = 1):
    lang= await db.get_language(telegram_id)
    API_URL = f"http://127.0.0.1:8000/{lang}/api"

    async with httpx.AsyncClient() as client:       
        r = await client.get(
            f"{API_URL}/my_bookings/?page={page}",
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            timeout=10
        )
        r.raise_for_status()
        return r.json()
    


async def fetch_zones(access_token: str, telegram_id: int, page: int = 1):
    lang = await db.get_language(telegram_id)
    url = f"http://127.0.0.1:8000/{lang}/api/zone/?page={page}"

    async with httpx.AsyncClient() as client:
        r = await client.get(
            url,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10
        )
        r.raise_for_status()
        return r.json()
    

async def fetch_rooms(access_token: str, telegram_id: int, zone_id: int, page: int = 1):
    lang = await db.get_language(telegram_id)
    url = f"http://127.0.0.1:8000/{lang}/api/room/?zone_id={zone_id}&page={page}"

    async with httpx.AsyncClient() as client:
        r = await client.get(
            url,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        r.raise_for_status()
        return r.json()
    

async def fetch_devices(access_token, telegram_id, zone_id, page=1):
    lang = await db.get_language(telegram_id)
    url = f"http://127.0.0.1:8000/{lang}/api/device/?zone_id={zone_id}&page={page}"

    async with httpx.AsyncClient() as client:
        r = await client.get(
            url,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        r.raise_for_status()
        return r.json()
    

BASE_URL = "http://127.0.0.1:8000"

async def book_device_api(access_token: str, lang: str, payload: dict) -> dict:
    url = f"{BASE_URL}/{lang}/api/booking_device/"   

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(
                url,
                headers={"Authorization": f"Bearer {access_token}"},
                json=payload
            )

    
        if r.status_code != 201:
            return {"ok": False, "status": r.status_code, "data": r.json()}

        data = r.json()

 
        booking_id = data.get("id") or data.get("booking_id")
        if not booking_id:
            return {"ok": False, "status": 201, "data": data, "error": "ID not found in response"}

        return {"ok": True, "status": 201, "data": data}

    except httpx.HTTPError as e:
        return {"ok": False, "status": 0, "error": str(e)}
    


async def fetch_device_detail(access_token: str, telegram_id: int, device_id: int):
    lang = await db.get_language(telegram_id)
    url = f"http://127.0.0.1:8000/{lang}/api/about_device/{device_id}/"

    async with httpx.AsyncClient() as client:
        r = await client.get(
            url,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        r.raise_for_status()
        return r.json()
    


async def book_room_api(access_token: str, lang: str, payload: dict) -> dict:
    url = f"{BASE_URL}/{lang}/api/booking_room/"

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(
                url,
                headers={"Authorization": f"Bearer {access_token}"},
                json=payload
            )

        if r.status_code != 201:
            return {
                "ok": False,
                "status": r.status_code,
                "data": r.json()
            }

        return {
            "ok": True,
            "status": 201,
            "data": r.json()
        }

    except httpx.HTTPError as e:
        return {
            "ok": False,
            "status": 0,
            "error": str(e)
        }
    
async def fetch_room_detail(access_token: str, telegram_id: int, room_id: int):
    lang = await db.get_language(telegram_id)
    url = f"{BASE_URL}/{lang}/api/about_room/{room_id}/"

    async with httpx.AsyncClient() as client:
        r = await client.get(
            url,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        r.raise_for_status()
        return r.json()