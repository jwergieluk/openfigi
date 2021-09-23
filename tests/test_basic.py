import unittest
import openfigi


class MyTestCase(unittest.TestCase):
    def test_invalid_api_type(self):
        self.assertRaises(ValueError, openfigi.OpenFigi, api_endpoint_type="V0")

    def test_wkn_ticker_anonymous_v1(self):
        ofg = openfigi.OpenFigi(api_endpoint_type="V1")
        self.assertIn("v1", ofg.url)
        self.assertNotIn("v2", ofg.url)
        ofg.enqueue_request(id_type='ID_WERTPAPIER', id_value='A0YEDG')

        response = ofg.fetch_response()
        self.assertTrue(type(response) is list)
        self.assertTrue(len(response) > 0)
        self.assertTrue(type(response[0]) is dict)
        self.assertTrue('data' in response[0].keys())
        self.assertTrue(len(response[0]['data']) > 0)


    def test_wkn_ticker_anonymous_v2(self):
        """Get an ETF by WKN and check if response makes sense"""
        ofg = openfigi.OpenFigi(api_endpoint_type="V2")
        self.assertIn("v2", ofg.url)
        self.assertNotIn("v1", ofg.url)
        ofg.enqueue_request(id_type='ID_WERTPAPIER', id_value='A0YEDG')

        response = ofg.fetch_response()
        self.assertTrue(type(response) is list)
        self.assertTrue(len(response) > 0)
        self.assertTrue(type(response[0]) is dict)
        self.assertTrue('data' in response[0].keys())
        self.assertTrue(len(response[0]['data']) > 0)

if __name__ == '__main__':
    unittest.main()
