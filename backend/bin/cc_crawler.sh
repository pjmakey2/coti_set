#!/bin/bash
#Cambios chaco
python mainline.py --crawler_exchange "cambios_chaco" --currency 'PYG'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'USD'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'BRL'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'EUR'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'CLP'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'UYU'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'COP'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'MXN'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'BOB'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'PEN'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'CAD'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'AUD'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'NOK'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'DKK'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'SEK'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'GBP'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'CHF'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'JPY'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'KWD'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'ILS'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'ZAR'
python mainline.py --crawler_exchange "cambios_chaco" --currency 'RUB'
#BCP
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "USD"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "EUR"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "GBP"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "JPY"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "CHF"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "CAD"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "AUD"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "CNY"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "BRL"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "ARS"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "CLP"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "MXN"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "UYU"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "COP"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "BOB"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "NZD"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "ZAR"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "SEK"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "DKK"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "NOK"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "SDR"
python mainline.py --crawler_exchange "bcp" --year 2023 --currency "XAU"
#Alberdi
python mainline.py --crawler_exchange "alberdi"
#Myd
python mainline.py --crawler_exchange "myd"
#Gnd
python mainline.py --crawler_exchange "gnb"
#Euroc
python mainline.py --crawler_exchange "euroc" --currency  'PYG' --stab 1
python mainline.py --crawler_exchange "euroc" --currency  'PYG' --stab 2
python mainline.py --crawler_exchange "euroc" --currency  'USD' --stab 1
python mainline.py --crawler_exchange "euroc" --currency  'USD' --stab 2
python mainline.py --crawler_exchange "euroc" --currency  'EUR' --stab 1
python mainline.py --crawler_exchange "euroc" --currency  'EUR' --stab 2
python mainline.py --crawler_exchange "euroc" --currency  'ARS' --stab 1
python mainline.py --crawler_exchange "euroc" --currency  'ARS' --stab 2
python mainline.py --crawler_exchange "euroc" --currency  'BRL' --stab 1
python mainline.py --crawler_exchange "euroc" --currency  'BRL' --stab 2
python mainline.py --crawler_exchange "euroc" --currency  'CLP' --stab 1
python mainline.py --crawler_exchange "euroc" --currency  'CLP' --stab 2
python mainline.py --crawler_exchange "euroc" --currency  'UYU' --stab 1
python mainline.py --crawler_exchange "euroc" --currency  'UYU' --stab 2
python mainline.py --crawler_exchange "euroc" --currency  'JPY' --stab 1
python mainline.py --crawler_exchange "euroc" --currency  'JPY' --stab 2
python mainline.py --crawler_exchange "euroc" --currency  'CAD' --stab 2
python mainline.py --crawler_exchange "euroc" --currency  'CAD' --stab 1
python mainline.py --crawler_exchange "euroc" --currency  'CHF' --stab 1
python mainline.py --crawler_exchange "euroc" --currency  'CHF' --stab 2
python mainline.py --crawler_exchange "euroc" --currency  'GBP' --stab 1
python mainline.py --crawler_exchange "euroc" --currency  'GBP' --stab 2
python mainline.py --crawler_exchange "euroc" --currency  'BOB' --stab 1
python mainline.py --crawler_exchange "euroc" --currency  'BOB' --stab 2
#Mundial
python mainline.py --crawler_exchange "mundialc"
#Vision banco
python mainline.py --crawler_exchange "visionc"
#Bonanza
python mainline.py --crawler_exchange "bonanza"
#La Moneda
python mainline.py --crawler_exchange "lamoneda"
#Set
python mainline.py --crawler_exchange "set"
#Familiar
python mainline.py --crawler_exchange "familiar"
#Expansion
python mainline.py --crawler_exchange "expansion" --year 2023 --month 8
python mainline.py --crawler_exchange "expansion" --year 2023 --month 7
python mainline.py --crawler_exchange "expansion" --year 2023 --month 6
#Yrendague
python mainline.py --crawler_exchange "yrendague" --bdate "2023-08-01" --odate "2023-08-31" --currency 'USD'
 python mainline.py --crawler_exchange "yrendague" --bdate "2023-08-01" --odate "2023-08-31" --currency 'BRL'
 python mainline.py --crawler_exchange "yrendague" --bdate "2023-08-01" --odate "2023-08-31" --currency 'ARS'
 python mainline.py --crawler_exchange "yrendague" --bdate "2023-08-01" --odate "2023-08-31" --currency 'EUR'
python mainline.py --crawler_exchange "yrendague" --bdate "2023-07-01" --odate "2023-07-31" --currency 'USD'
 python mainline.py --crawler_exchange "yrendague" --bdate "2023-07-01" --odate "2023-07-31" --currency 'BRL'
 python mainline.py --crawler_exchange "yrendague" --bdate "2023-07-01" --odate "2023-07-31" --currency 'ARS'
 python mainline.py --crawler_exchange "yrendague" --bdate "2023-07-01" --odate "2023-07-31" --currency 'EUR' 
 #Triple C
 python mainline.py --crawler_exchange "triplec" --year 2023 --month 8
 python mainline.py --crawler_exchange "triplec" --year 2023 --month 7




