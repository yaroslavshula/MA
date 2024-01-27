import requests
import unittest
import json

theater_url = 'http://localhost:8000'
tickets_url = 'http://localhost:8001'
add_show_url = f"{theater_url}/add_show"
get_show_by_id_url = f"{theater_url}/get_show_by_id"
delete_show_url = f"{theater_url}/delete_show"

show_data = {
    "id": 3,
    "type": "comedy",
    "theater_id": 4
}


class TestIntegration(unittest.TestCase):

    def test_show_get(self):
        requests.post(add_show_url, json=show_data)
        res = requests.get(f"{get_show_by_id_url}?show_id=3")
        res = json.loads(res.text)
        self.assertEqual(res['id'], 3)
        self.assertEqual(res['type'], 'comedy')
        self.assertEqual(res['theater_id'], 4)

    def test_delete_show(self):
        res = requests.delete(f"{delete_show_url}?show_id=2")


if __name__ == '__main__':
    unittest.main()
