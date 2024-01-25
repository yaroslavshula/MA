import unittest
import requests
import json

theater_url = "http://localhost:8000"
tickets_url = "http://localhost:8001"
get_show_by_id_url = f"{theater_url}/get_show_by_id"


class TestIntegration(unittest.TestCase):

    def test_theater_service_connection(self):
        r = requests.get(f"{theater_url}/healthCheck", verify=False)
        self.assertEqual(r.status_code, 200)

    def test_tickets_service_connection(self):
        r = requests.get(f"{tickets_url}/healthCheck", verify=False)
        self.assertEqual(r.status_code, 200)

    def test_get_show(self):
        res = requests.get(f"{get_show_by_id_url}?show_id=1", verify=False)
        res = json.loads(res.text)
        self.assertEqual(res['type'], 'Musical')
        self.assertEqual(res['theater_id'], 2)


if __name__ == '__main__':
    unittest.main()
