import unittest
import openfigi


class MyTestCase(unittest.TestCase):
    def test_wkn_ticker_anonymous(self):
        """Get an ETF by WKN and check if response makes sense"""
        ofg = openfigi.OpenFigi()
        ofg.enqueue_request(id_type='ID_WERTPAPIER', id_value='A0YEDG')

        response = ofg.fetch_response()
        self.assertTrue(type(response) is list)
        self.assertTrue(len(response) > 0)
        self.assertTrue(type(response[0]) is dict)
        self.assertTrue('data' in response[0].keys())
        self.assertTrue(len(response[0]['data']) > 0)

if __name__ == '__main__':
    unittest.main()
