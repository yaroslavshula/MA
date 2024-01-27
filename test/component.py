import requests
import pytest

theater_url = 'https://localhost:8000'
tickets_url = 'https://localhost:8001'
add_show_url = f"{theater_url}/add_show"
get_show_by_id_url = f"{theater_url}/get_show_by_id"


show_data = {
    "id": 1,
    "type": "comedy",
    "theater_id": 4
}

r = requests.get(f"{theater_url}/healthCheck", verify=False)
r = requests.get(f"{tickets_url}/healthCheck", verify=False)

def test_show_get():
    pytest.assume(requests.post(add_show_url, json=show_data) == 200)
    res = requests.get(f"{get_show_by_id_url}/{show_data['id']}")
    pytest.assume('type' in res.keys())
    pytest.assume('theater_id' in res.keys())