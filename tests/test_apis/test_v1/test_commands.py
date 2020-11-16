import json


def test_get_command(client):
    resp = client.get("/v1/commands", params={"name": "wat", "game": 0})
    assert resp.json() == json.loads(
        """{
  "name": "wat",
  "template": "new wat text here",
  "game": 0,
  "cooldown": 0,
  "required_role": 0
}"""
    )
