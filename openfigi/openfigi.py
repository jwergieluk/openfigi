import logging
import requests
import time


class OpenFigi:
    id_types = {'ID_ISIN': 'ISIN',
                'ID_BB_UNIQUE': 'Unique Bloomberg Identifier',
                'ID_SEDOL': 'Sedol Number',
                'ID_COMMON': 'Common Code',
                'ID_WERTPAPIER': 'Wertpapierkennnummer/WKN',
                'ID_CUSIP': 'CUSIP',
                'ID_CINS': 'CINS - CUSIP International Numbering System',
                'ID_BB': 'ID BB',
                'ID_ITALY': 'Italian Identifier Number',
                'ID_EXCH_SYMBOL': 'Local Exchange Security Symbol',
                'ID_FULL_EXCHANGE_SYMBOL': 'Full Exchange Symbol',
                'COMPOSITE_ID_BB_GLOBAL': 'Composite Financial Instrument Global Identifier',
                'ID_BB_GLOBAL_SHARE_CLASS_LEVEL': 'Share Class Financial Instrument Global Identifier',
                'ID_BB_SEC_NUM_DES': 'Security ID Number Description',
                'ID_BB_GLOBAL': 'Financial Instrument Global Identifier (FIGI)',
                'TICKER': 'Ticker',
                'ID_CUSIP_8_CHR': 'CUSIP (8 Characters Only)',
                'OCC_SYMBOL': 'OCC Symbol',
                'UNIQUE_ID_FUT_OPT': 'Unique Identifier for Future Option',
                'OPRA_SYMBOL': 'OPRA Symbol',
                'TRADING_SYSTEM_IDENTIFIER': 'Trading System Identifier'}

    def __init__(self, key=None):
        self.logger = logging.getLogger(__name__)
        self.url = 'https://api.openfigi.com/v1/mapping'
        self.api_key = key
        self.headers = {'Content-Type': 'text/json', 'X-OPENFIGI-APIKEY': key}
        self.request_items = []
        self.response_items = []
        self.max_tickers_per_request = 100

    def enqueue_request(self, id_type, id_value, exchange_code='', mic_code='', currency=''):
        query = {'idType': id_type, 'idValue': id_value}
        if id_type not in self.id_types.keys():
            self.logger.error('Bad id_type.')
            return
        if len(exchange_code) > 0:
            query['exchCode'] = exchange_code
        if len(mic_code) > 0:
            query['micCode'] = mic_code
        if len(currency) > 0:
            query['currency'] = currency

        self.request_items.append(query)

    def __get_batch(self, batch_request_items, remove_missing=False):
        response = requests.post(self.url, json=batch_request_items, headers=self.headers)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            if response.status_code == 400:
                self.logger.error('The request body is not an array.')
            if response.status_code == 401:
                self.logger.error('The API_KEY is invalid.')
            if response.status_code == 404:
                self.logger.error('The requested path is invalid.')
            if response.status_code == 405:
                self.logger.error('The HTTP verb is not POST.')
            if response.status_code == 406:
                self.logger.error('The server does not support the requested Accept type.')
            if response.status_code == 413:
                self.logger.error('The request exceeds the max number of identifiers support in one request.')
            if response.status_code == 429:
                self.logger.error('Too Many Requests.')
            if response.status_code == 500:
                self.logger.error('Internal Server Error.')
            return None

        batch_response_items = response.json()
        if len(batch_response_items) == len(batch_request_items):
            for (i, item) in enumerate(batch_response_items):
                item.update(batch_request_items[i])
        else:
            self.logger.warning('Number of request and response items do not match. Dumping the results only.')
        if remove_missing:
            for item in batch_response_items:
                if 'error' not in item.keys():
                    self.response_items.append(item)
        else:
            self.response_items += batch_response_items

    def fetch_response(self, remove_missing=False):
        """ Partitions the requests into batches and attempts to get responses.

            See https://www.openfigi.com/api#rate-limiting for a detailed explanation.
        """
        if len(self.request_items) < 100:
            self.__get_batch(self.request_items, remove_missing)
        else:
            self.__get_batch(self.request_items[-100:], remove_missing)
            self.request_items = self.request_items[:-100]
            time.sleep(0.6)
            self.fetch_response(remove_missing)

        self.request_items.clear()
        return self.response_items
