import asyncio

from src.dependencies import get_db


async def send_emails_bookings_today_checkin():
    async for db in get_db():
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")


async def run_send_email_regularly():
    while True:
        await send_emails_bookings_today_checkin()
        await asyncio.sleep(5)
