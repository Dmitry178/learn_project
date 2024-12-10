async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    print(f"{response.json()=}")

    assert response.status_code == 200


async def test_post_hotels(ac):
    response = await ac.post(
        "/facilities",
        json={
            "title": "Кукарача"
        }
    )
    print(f"{response.json()=}")

    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    assert response.json()["data"]["title"] == "Кукарача"
