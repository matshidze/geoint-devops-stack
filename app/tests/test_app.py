from app.app import create_app

def test_home_ok():
    app = create_app(testing=True)
    client = app.test_client()
    r = client.get("/")
    assert r.status_code == 200

def test_submit_flow():
    app = create_app(testing=True)
    client = app.test_client()
    r = client.post("/submit", data={"text": "hello"}, follow_redirects=True)
    assert r.status_code == 200
    assert b"hello" in r.data
