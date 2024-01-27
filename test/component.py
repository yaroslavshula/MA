import requests
import unittest

theater_url = 'http://localhost:8000'
tickets_url = 'http://localhost:8001'
add_show_url = f"{theater_url}/add_show"
get_show_by_id_url = f"{theater_url}/get_show_by_id"


show_data = {
    "id": 1,
    "type": "comedy",
    "theater_id": 4
}

class TestIntegration(unittest.TestCase):

    def test_show_get(self):
        requests.post(add_show_url, json=show_data)
        res = requests.get(f"{get_show_by_id_url}/{show_data['id']}")
        self.assertEqual(res['id'], )
        self.assertEqual(res['type'], 'comedy')
        self.assertEqual(res['theater_id'], 4)

    def test_delete_show(self):
        res = requests.delete(f"{theater_url}/{show_data['id']}")
        self.assertEqual(res, "deleted")

if __name__ == '__main__':
    unittest.main()