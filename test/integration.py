import unittest
import requests
from time import sleep
import json

theater_service = "http://localhost:8000"
tickets_service = "http://localhost:8001"


class TestIntegration(unittest.TestCase):

    def test_station_service_connection(self):
        r = requests.get(f"{theater_service}/health")
        self.assertEqual(r.status_code, 200)

    def test_ticket_service_connection(self):
        r = requests.get(f"{tickets_service}/health")
        self.assertEqual(r.status_code, 200)

    def test_get_show(self):
        res = requests.get(f"{theater_service}/get_show_by_id/?show_id=1", verify=False)
        res = json.loads(res.text)
        self.assertEqual(res['type'], 'Musical')
        self.assertEqual(res['theater_id'], 2)


if __name__ == '__main__':
    unittest.main()
