from openfigi import OpenFigi
import click
import logging
import os
import json


root_logger = logging.getLogger('')
root_logger.setLevel(logging.INFO)
console = logging.StreamHandler()
formatter = logging.Formatter('# %(asctime)s %(levelname)s: %(name)s: %(message)s', datefmt='%Y%m%d %H:%M:%S')
console.setFormatter(formatter)
root_logger.addHandler(console)


@click.command()
@click.argument('id_type')
@click.argument('id_value')
@click.option('--exchange_code', default='', help='An optional exchange code if it applies (cannot use with mic_code).')
@click.option('--mic_code', default='',
              help='An optional ISO market identification code(MIC) if it applies (cannot use with exchange_code).')
@click.option('--currency', default='', help='An optional currency if it applies.')
def call_figi(id_type, id_value, exchange_code, mic_code, currency):
    """
    Calls OpenFIGI API with the specified arguments

    ID_TYPE must be one of the following:
    ID_ISIN, ID_BB_UNIQUE, ID_SEDOL, ID_COMMON, ID_WERTPAPIER, ID_CUSIP,
    ID_BB, ID_ITALY, ID_EXCH_SYMBOL, ID_FULL_EXCHANGE_SYMBOL, COMPOSITE_ID_BB_GLOBAL,
    ID_BB_GLOBAL_SHARE_CLASS_LEVEL, ID_BB_SEC_NUM_DES, ID_BB_GLOBAL, TICKER,
    ID_CUSIP_8_CHR, OCC_SYMBOL, UNIQUE_ID_FUT_OPT, OPRA_SYMBOL, TRADING_SYSTEM_IDENTIFIER
    """
    key = None
    if 'openfigi_key' in os.environ:
        key = os.environ['openfigi_key']
    else:
        root_logger.info('openfigi_key variable not present in the environment. Using anonymous access.')
    figi = OpenFigi(key)
    figi.enqueue_request(id_type, id_value, exchange_code, mic_code, currency)
    text = figi.fetch_response()
    click.echo(json.dumps(text, sort_keys=True, indent=4))

