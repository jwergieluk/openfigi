#!/bin/env python3

import requests
import logging
import os
import json
import click


class OpenFigi:
    id_types = {'ID_ISIN': 'ISIN',
                'ID_BB_UNIQUE': 'Unique Bloomberg Identifier',
                'ID_SEDOL': 'Sedol Number',
                'ID_COMMON': 'Common Code',
                'ID_WERTPAPIER': 'Wertpapierkennnummer/WKN',
                'ID_CUSIP': 'CUSIP',
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
        self.data = []

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

        self.data.append(query)

    def fetch_response(self):
        self.logger.debug(self.data)
        response = requests.post(self.url, json=self.data, headers=self.headers)
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
        return response.json()


@click.command()
@click.argument('id_type')
@click.argument('id_value')
@click.option('--exchange_code', default='', help='An optional exchange code if it applies(cannot use with mic_code).')
@click.option('--mic_code', default='',
              help='An optional ISO market identification code(MIC) if it applies(cannot use with exchange_code).')
@click.option('--currency', default='', help='An optional currency if it applies.')
def call_figi(id_type, id_value, exchange_code, mic_code, currency):
    key = None
    if 'openfigi_key' in os.environ:
        key = os.environ['openfigi_key']
        logger.info('openfigi_key variable not present in env. Using anonymous access.')
    figi = OpenFigi(key)
    figi.enqueue_request(id_type, id_value, exchange_code, mic_code, currency)
    text = figi.fetch_response()
    click.echo(json.dumps(text, sort_keys=True, indent=4))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    call_figi()
