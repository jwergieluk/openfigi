import logging
import requests
import time


logger = logging.getLogger(__name__)

BASE_URLS = {"V1": "https://api.openfigi.com/v1/mapping", "V2": "https://api.openfigi.com/v2/mapping"}


class OpenFigi:
    """This class tries to map the interface defined in https://www.openfigi.com/api"""

    id_types = {
        "BASE_TICKER": "An indistinct identifier which may be linked to multiple instruments. May need to be combined with other values to identify a unique instrument.",
        "COMPOSITE_ID_BB_GLOBAL": "Composite Financial Instrument Global Identifier - The Composite Financial Instrument Global Identifier (FIGI) enables users to link multiple FIGIs at the trading venue level within the same country or market in order to obtain an aggregated view for an instrument within that country or market.",
        "ID_BB": "A legacy Bloomberg identifier.",
        "ID_BB_8_CHR": "A legacy Bloomberg identifier (8 characters only).",
        "ID_BB_GLOBAL": "Financial Instrument Global Identifier (FIGI) - An identifier that is assigned to instruments of all asset classes and is unique to an individual instrument. Once issued, the FIGI assigned to an instrument will not change.",
        "ID_BB_GLOBAL_SHARE_CLASS_LEVEL": "Share Class Financial Instrument Global Identifier - A Share Class level Financial Instrument Global Identifier is assigned to an instrument that is traded in more than one country. This enables users to link multiple Composite FIGIs for the same instrument in order to obtain an aggregated view for that instrument across all countries (globally).",
        "ID_BB_SEC_NUM_DES": "Security ID Number Description - Descriptor for a financial instrument. Similar to the ticker field, but will provide additional metadata data.",
        "ID_BB_UNIQUE": "Unique Bloomberg Identifier - A legacy, internal Bloomberg identifier.",
        "ID_CINS": "CINS - CUSIP International Numbering System.",
        "ID_COMMON": "Common Code - A nine digit identification number.",
        "ID_CUSIP": "CUSIP - Committee on Uniform Securities Identification Procedures.",
        "ID_CUSIP_8_CHR": "CUSIP (8 Characters Only) - Committee on Uniform Securities Identification Procedures.",
        "ID_EXCH_SYMBOL": "Local Exchange Security Symbol - Local exchange security symbol.",
        "ID_FULL_EXCHANGE_SYMBOL": "Full Exchange Symbol - Contains the exchange symbol for futures, options, indices inclusive of base symbol and other security elements.",
        "ID_ISIN": "ISIN - International Securities Identification Number.",
        "ID_ITALY": "Italian Identifier Number - The Italian Identification number consisting of five or six digits.",
        "ID_SEDOL": "Sedol Number - Stock Exchange Daily Official List.",
        "ID_SHORT_CODE": "An exchange venue specific code to identify fixed income instruments primarily traded in Asia.",
        "ID_TRACE": "Trace eligible bond identifier issued by FINRA.",
        "ID_WERTPAPIER": "Wertpapierkennnummer/WKN - German securities identification code.",
        "OCC_SYMBOL": "OCC Symbol - A twenty-one character option symbol standardized by the Options Clearing Corporation (OCC) to identify a U.S. option.",
        "OPRA_SYMBOL": "OPRA Symbol - Option symbol standardized by the Options Price Reporting Authority (OPRA) to identify a U.S. option.",
        "TICKER": "Ticker - Ticker is a specific identifier for a financial instrument that reflects common usage.",
        "TRADING_SYSTEM_IDENTIFIER": "Trading System Identifier - Unique identifier for the instrument as used on the source trading system.",
        "UNIQUE_ID_FUT_OPT": "Unique Identifier for Future Option - Bloomberg unique ticker with logic for index, currency, single stock futures, commodities and commodity options.",
    }

    def __init__(self, key=None, api_version="V1"):
        if api_version not in BASE_URLS:
            raise ValueError("Unsupported API version. Supported versions: {0}" "".format(", ".join(BASE_URLS.keys())))
        self.url = BASE_URLS[api_version]
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

    def _get_batch(self, batch_request_items, remove_missing=False):
        response = requests.post(self.url, json=batch_request_items, headers=self.headers)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            if response.status_code == 400:
                logger.error('The request body is not an array.')
            if response.status_code == 401:
                logger.error('The API_KEY is invalid.')
            if response.status_code == 404:
                logger.error('The requested path is invalid.')
            if response.status_code == 405:
                logger.error('The HTTP verb is not POST.')
            if response.status_code == 406:
                logger.error('The server does not support the requested Accept type.')
            if response.status_code == 413:
                logger.error('The request exceeds the max number of identifiers support in one request.')
            if response.status_code == 429:
                logger.error('Too Many Requests.')
            if response.status_code == 500:
                logger.error('Internal Server Error.')
            return None

        batch_response_items = response.json()
        if len(batch_response_items) == len(batch_request_items):
            for (i, item) in enumerate(batch_response_items):
                item.update(batch_request_items[i])
        else:
            logger.warning('Number of request and response items do not match. Dumping the results only.')
        if remove_missing:
            for item in batch_response_items:
                if 'error' not in item.keys():
                    self.response_items.append(item)
        else:
            self.response_items += batch_response_items

    def fetch_response(self, remove_missing=False):
        """Partitions the requests into batches and attempts to get responses.

        See https://www.openfigi.com/api#rate-limiting for a detailed explanation.
        """
        if len(self.request_items) < 100:
            self._get_batch(self.request_items, remove_missing)
        else:
            self._get_batch(self.request_items[-100:], remove_missing)
            self.request_items = self.request_items[:-100]
            time.sleep(0.6)
            self.fetch_response(remove_missing)

        self.request_items.clear()
        return self.response_items
