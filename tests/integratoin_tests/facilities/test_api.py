async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    print(f"{response.json()=}")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_post_hotels(ac):
    title = "Кукарача"
    response = await ac.post(
        "/facilities",
        json={
            "title": title
        }
    )
    print(f"{response.json()=}")

    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, dict)
    assert result["status"] == "OK"
    assert "data" in result
    assert result["data"]["title"] == title
