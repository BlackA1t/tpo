import time


def _assert_json_content_type(resp) -> None:
    ct = resp.headers.get("Content-Type", "")
    assert "application/json" in ct, f"Unexpected Content-Type: {ct}"


def _assert_post_shape(post: dict) -> None:
    assert set(post.keys()) == {"userId", "id", "title", "body"}

    assert isinstance(post["userId"], int)
    assert isinstance(post["id"], int) and post["id"] >= 0

    assert isinstance(post["title"], str) and len(post["title"]) > 0
    assert isinstance(post["body"], str) and len(post["body"]) > 0


def test_get_posts_list(session, base_url):
    start = time.time()
    resp = session.get(f"{base_url}/posts")
    elapsed_ms = (time.time() - start) * 1000

    assert resp.status_code == 200
    _assert_json_content_type(resp)
    assert elapsed_ms < 5000, f"Response too slow: {elapsed_ms:.1f}ms"

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0

    for post in data[:20]:
        assert isinstance(post, dict)
        _assert_post_shape(post)


def test_create_post_post_method(session, base_url):
    payload = {"title": "test title", "body": "test body", "userId": 1}

    start = time.time()
    resp = session.post(f"{base_url}/posts", json=payload)
    elapsed_ms = (time.time() - start) * 1000

    assert resp.status_code == 201, f"Expected 201, got {resp.status_code}"
    _assert_json_content_type(resp)
    assert elapsed_ms < 5000, f"Response too slow: {elapsed_ms:.1f}ms"

    data = resp.json()
    assert isinstance(data, dict)

    assert set(data.keys()) == {"userId", "id", "title", "body"}
    _assert_post_shape(data)


def test_update_post_put_method(session, base_url):
    payload = {"id": 1, "title": "updated title", "body": "updated body", "userId": 1}

    start = time.time()
    resp = session.put(f"{base_url}/posts/1", json=payload)
    elapsed_ms = (time.time() - start) * 1000

    assert resp.status_code == 200
    _assert_json_content_type(resp)
    assert elapsed_ms < 5000, f"Response too slow: {elapsed_ms:.1f}ms"

    data = resp.json()
    assert isinstance(data, dict)
    assert set(data.keys()) == {"userId", "id", "title", "body"}
    _assert_post_shape(data)

    assert data["id"] == 1
    assert data["userId"] == 1
    assert data["title"] == "updated title"
    assert data["body"] == "updated body"
