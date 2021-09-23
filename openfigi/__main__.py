from openfigi import OpenFigi, BASE_URLS
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
@click.argument('id_type', nargs=1)
@click.argument('id_values', nargs=-1)
@click.option('--exchange-code', default='', help='An optional exchange code if it applies (cannot use with mic_code).')
@click.option(
    '--mic-code',
    default='',
    help='An optional ISO market identification code(MIC) if it applies (cannot use with exchange_code).',
)
@click.option('--currency', default='', help='An optional currency if it applies.')
@click.option('--remove-missing/--no-remove-missing', default=False, help='Remove records with errors.')
@click.option(
    '--api-version',
    default='V1',
    help="The OpenFIGI API version to utilize.",
    type=click.Choice(list(BASE_URLS.keys())),
)
def call_figi(id_type, id_values, exchange_code, mic_code, currency, remove_missing, api_version):
    """Calls OpenFIGI API

    ID_TYPE must be one of the following:
    BASE_TICKER COMPOSITE_ID_BB_GLOBAL ID_BB ID_BB_8_CHR ID_BB_GLOBAL ID_BB_GLOBAL_SHARE_CLASS_LEVEL ID_BB_SEC_NUM_DES
    ID_BB_UNIQUE ID_CINS ID_COMMON ID_CUSIP ID_CUSIP_8_CHR ID_EXCH_SYMBOL ID_FULL_EXCHANGE_SYMBOL ID_ISIN ID_ITALY
    ID_SEDOL ID_SHORT_CODE ID_TRACE ID_WERTPAPIER OCC_SYMBOL OPRA_SYMBOL TICKER TRADING_SYSTEM_IDENTIFIER
    UNIQUE_ID_FUT_OPT

    ID_VALUES is a list of (space separated) ids corresponding to the specified ID_TYPE.
    """
    key = None
    if 'openfigi_key' in os.environ:
        key = os.environ['openfigi_key']
    else:
        root_logger.info('openfigi_key variable not present in the environment. Using anonymous access.')
    figi = OpenFigi(key, api_version=api_version)
    for id_value in id_values:
        figi.enqueue_request(id_type.upper(), id_value, exchange_code.upper(), mic_code.upper(), currency.upper())
    text = figi.fetch_response(remove_missing)
    click.echo(json.dumps(text, sort_keys=True, indent=4))
