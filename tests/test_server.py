from fastapi.testclient import TestClient
from mcp_fastmcp_starter.server import app

client = TestClient(app)

def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_list_tools():
    r = client.get("/tools")
    assert r.status_code == 200
    body = r.json()
    names = {t["name"] for t in body["tools"]}
    assert "sayHello" in names
    assert "reverse" in names

def test_invoke_sayhello():
    r = client.post(
        "/invoke",
        json={"tool": "sayHello", "args": {"name": "Dennis"}, "trace_id": "t1"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["result"]["message"] == "Hello, Dennis."
    assert body["trace_id"] == "t1"

def test_invoke_reverse():
    r = client.post(
        "/invoke",
        json={"tool": "reverse", "args": {"text": "abc"}},
    )
    body = r.json()
    assert body["ok"] is True
    assert body["result"]["reversed"] == "cba"
    assert body["result"]["length"] == 3

def test_unknown_tool():
    r = client.post("/invoke", json={"tool": "nope"})
    body = r.json()
    assert body["ok"] is False
    assert "Unknown tool" in body["error"]
