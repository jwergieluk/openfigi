# openfigi

Simple wrapper and a command-line tool for Bloomberg's OpenFIGI API.

The API specification is located at https://www.openfigi.com/api

## Usage

    import openfigi
    openfigi = OpenFigi('abcdefghijklmnopqrstuvwxyz')
    openfigi.enqueue_request(id_type='ID_WERTPAPIER', id_value='XM91CQ', mic_code='EUWX')
    print(openfigi.fetch_responce())

## Cli usage

    > ofg --help
    Usage: ofg [OPTIONS] ID_TYPE [ID_VALUES]...

      Calls OpenFIGI API with the specified arguments

      ID_TYPE must be one of the following: ID_ISIN, ID_BB_UNIQUE, ID_SEDOL,
      ID_COMMON, ID_WERTPAPIER, ID_CUSIP, ID_BB, ID_ITALY, ID_EXCH_SYMBOL,
      ID_FULL_EXCHANGE_SYMBOL, COMPOSITE_ID_BB_GLOBAL,
      ID_BB_GLOBAL_SHARE_CLASS_LEVEL, ID_BB_SEC_NUM_DES, ID_BB_GLOBAL, TICKER,
      ID_CUSIP_8_CHR, OCC_SYMBOL, UNIQUE_ID_FUT_OPT, OPRA_SYMBOL,
      TRADING_SYSTEM_IDENTIFIER

      ID_VALUES is a list of (space separated) id corresponding to ID_TYPE.

    Options:
      --exchange_code TEXT  An optional exchange code if it applies (cannot use
                            with mic_code).
      --mic_code TEXT       An optional ISO market identification code(MIC) if it
                            applies (cannot use with exchange_code).
      --currency TEXT       An optional currency if it applies.
      --help                Show this message and exit.

Sample call:

    $ ofg --mic_code EUWX ID_WERTPAPIER XM91CQ
    [
        {
            "data": [
                {
                    "compositeFIGI": "BBG00BP73295",
                    "exchCode": "GW",
                    "figi": "BBG00BP732P7",
                    "marketSector": "Equity",
                    "name": "DEUTSCH-PW17 DAX INDEX",
                    "securityType": "Index WRT",
                    "shareClassFIGI": null,
                    "ticker": "XM91CQ",
                    "uniqueID": "EQ0000000047042754",
                    "uniqueIDFutOpt": null
                }
            ]
        }
    ]

The cli tool searches for the `openfigi_key` environment variable and uses it to
authenticate the API calls. If `openfigi_key` is not defined, an anonymous access is used.

#### Trademarks

'OPENFIGI', 'BLOOMBERG', and 'BLOOMBERG.COM' are trademarks and service marks of
Bloomberg Finance L.P., a Delaware limited partnership, or its subsidiaries.

#### Copyright and license

MIT License: see LICENSE file for details.

Copyright (c) 2016-2017 Julian Wergieluk
