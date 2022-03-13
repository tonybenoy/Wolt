from fastapi.testclient import TestClient

from src.constants import MAXTIME, MINTIME
from src.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/test")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["result"] == "success"
    assert response_json["msg"] == "It works!"


def test_post_humanize_open_hours_invalid_timestamp_not_integer():
    payload = {"monday": [{"type": "open", "value": "not_integer"}]}
    response = client.post("/humanize-open-hours/", json=payload)
    assert response.status_code == 422
    response_json = response.json()
    assert response_json["detail"][0]["msg"] == "value is not a valid integer"
    assert response_json["detail"][0]["type"] == "type_error.integer"


def test_post_humanize_open_hours_invalid_timestamp_lower():
    payload = {"monday": [{"type": "open", "value": 0}]}
    response = client.post("/humanize-open-hours/", json=payload)
    assert response.status_code == 422
    response_json = response.json()
    assert (
        response_json["detail"][0]["msg"]
        == f"Timestamp not in range. Should be between {MINTIME} and {MAXTIME}"
    )
    assert response_json["detail"][0]["type"] == "value_error"


def test_post_humanize_open_hours_invalid_timestamp_greater():
    payload = {"monday": [{"type": "open", "value": 66666}]}
    response = client.post("/humanize-open-hours/", json=payload)
    assert response.status_code == 422
    response_json = response.json()
    assert (
        response_json["detail"][0]["msg"]
        == f"Timestamp not in range. Should be between {MINTIME} and {MAXTIME}"
    )
    assert response_json["detail"][0]["type"] == "value_error"


def test_post_humanize_open_hours_invalid_type():
    payload = {"monday": [{"type": "opened", "value": 66666}]}
    response = client.post("/humanize-open-hours/", json=payload)
    assert response.status_code == 422
    response_json = response.json()
    assert "permitted: 'open', 'close" in response_json["detail"][0]["msg"]
    assert response_json["detail"][0]["type"] == "type_error.enum"


def test_post_humanize_open_hours_success():
    payload = {
        "monday": [],
        "tuesday": [
            {"type": "open", "value": 36000},
            {"type": "close", "value": 64800},
        ],
        "wednesday": [],
        "thursday": [
            {"type": "open", "value": 37800},
            {"type": "close", "value": 64800},
        ],
        "friday": [{"type": "open", "value": 36000}],
        "saturday": [
            {"type": "close", "value": 3600},
            {"type": "open", "value": 36000},
        ],
        "sunday": [
            {"type": "close", "value": 3600},
            {"type": "open", "value": 43200},
            {"type": "close", "value": 75600},
        ],
    }
    response = client.post("/humanize-open-hours/", json=payload)
    assert response.status_code == 200
    response_text = response.text
    assert "Monday : Closed" in response_text
    assert "Tuesday : 03:30 PM - 11:30 PM" in response_text
    assert "Wednesday : Closed" in response_text
    assert "Thursday : 04:00 PM - 11:30 PM" in response_text
    assert "Friday : 03:30 PM - 06:30 AM" in response_text
    assert "Saturday : 03:30 PM - 06:30 AM" in response_text
    assert "Sunday : 05:30 PM - 02:30 AM" in response_text


def test_post_humanize_open_hours_unclosed_restauant():
    payload = {
        "monday": [],
        "tuesday": [
            {"type": "open", "value": 36000},
            {"type": "close", "value": 64800},
        ],
        "wednesday": [],
        "thursday": [
            {"type": "open", "value": 37800},
            {"type": "close", "value": 64800},
        ],
        "friday": [{"type": "open", "value": 36000}],
        "saturday": [{"type": "open", "value": 36000}],
        "sunday": [
            {"type": "close", "value": 3600},
            {"type": "open", "value": 43200},
            {"type": "close", "value": 75600},
        ],
    }
    response = client.post("/humanize-open-hours/", json=payload)
    assert response.status_code == 422
    response_json = response.json()
    assert "Closing time not available" == response_json["detail"]
