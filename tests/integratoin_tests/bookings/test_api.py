async def test_add_booking(db, aac):
    room_id = (await db.rooms.get_all())[0].id

    response = await aac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": "2024-08-01",
            "date_to": "2024-08-10",
        }
    )
    assert response.status_code == 200

    result = response.json()
    assert isinstance(result, dict)
    assert result["status"] == "OK"
    assert "data" in result
