# openfigi

Simple wrapper and a command-line tool for Bloomberg's OpenFIGI API.

The API specification is located under [https://www.openfigi.com/api].

## Usage

    import openfigi
    openfigi = OpenFigi('abcdefghijklmnopqrstuvwxyz')
    openfigi.enqueue_request(id_type='ID_WERTPAPIER', id_value='XM91CQ', mic_code='EUWX')
    print(openfigi.fetch_responce())

## Cli usage

    $ openfigi.py --help
    Usage: openfigi.py [OPTIONS] ID_TYPE ID_VALUE
    
    Options:
      --exchange_code TEXT  An optional exchange code if it applies(cannot use
                            with mic_code).
      --mic_code TEXT       An optional ISO market identification code(MIC) if it
                            applies(cannot use with exchange_code).
      --currency TEXT       An optional currency if it applies.
      --help                Show this message and exit.

Sample call:

    $ openfigi.py --mic_code EUWX ID_WERTPAPIER XM91CQ
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

The cli tool searches for 'openfigi_key' environment variable and uses it to
authenticate. If this fails, an anonymous access is used. 
