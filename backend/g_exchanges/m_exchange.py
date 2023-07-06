from datetime import datetime, date
from sqlalchemy.orm import Session
import urllib3 as htr, json, logging
from urllib.parse import urlencode
from bs4 import BeautifulSoup as bs
from db.g_session import db_clises
from db.uw_exchange import ex_query, ex_bulk_insert
from sts import settings as sst
import re

MODULE = "models.m_finance"
MODEL = "Exchange"


def triplec_process(group_source: str, year, month):
    source = 'TRIPLEC'
    currency = 'USD'
    pps = {
        'idsucursal': 1,
        'year': year, 'month': month
    }
    rsp = htr.request(
            'GET',
            sst.TRIPLEC,
            fields=pps,
            headers=sst.GEN_HEADERS
    )
    cc = rsp.json()
    entries = []
    
    for kk, dd in cc.items():
        cdate = datetime.strptime(dd.get('fecha'), '%d-%m-%Y').date()
        buy = dd.get('compra')
        sale = dd.get('venta')
        with db_clises() as ses:
            d = check_exchange_dup(
                    db = ses,
                    source = source,
                    currency = currency,
                    odate = cdate,
                    buy = buy,
                    sales = sale
            )
            if not d:
                entries.append(
                    {
                        "group_source": group_source,
                        "source": source,
                        "currency": currency,
                        "sales": sale,
                        "buy": buy,
                        "year": cdate.year,
                        "month": cdate.month,
                        "date": cdate,
                    }
                )
    if entries:
        with db_clises() as ses:
            ex_bulk_insert(ses, MODULE, MODEL, entries)    
    


def yrendague_process(group_source:str, bdate, odate, currency):
    source = 'YRENDAGUE'
    currs = {
        'USD': 1,'BRL': 2,'ARS': 3,'EUR': 4,
    }
    pps = {
        'action': 'get_cotizaciones',
        'fecha_desde': datetime.strptime(bdate, '%Y-%m-%d').strftime('%d/%m/%Y'),
        'fecha_hasta': datetime.strptime(odate, '%Y-%m-%d').strftime('%d/%m/%Y'),
        'idmoneda': currs.get(currency)
    }
    rsp = htr.request('POST',
            sst.YRENDAGUE,
            fields=pps,
    )
    cc = rsp.json()
    entries = []
    for dd in cc.get('datos'):
        cdate = datetime.strptime(dd.get('fecha'), '%Y-%m-%d %H:%M:%S').date()
        buy = dd.get('p_compra')
        sale = dd.get('p_venta')
        with db_clises() as ses:
            d = check_exchange_dup(
                    db = ses,
                    source = source,
                    currency = currency,
                    odate = cdate,
                    buy = buy,
                    sales = sale
            )
            if not d:
                entries.append(
                    {
                        "group_source": group_source,
                        "source": source,
                        "currency": currency,
                        "sales": sale,
                        "buy": buy,
                        "year": cdate.year,
                        "month": cdate.month,
                        "date": cdate,
                    }
                )
    if entries:
        with db_clises() as ses:
            ex_bulk_insert(ses, MODULE, MODEL, entries)

def expansion_process(group_source: str, year, month):
    source = 'EXPANSION'
    pps = {'dr': f'{year}-{month.zfill(2)}'}
    rsp = htr.request('GET',
            sst.EXPANSION,
            fields=pps,
            headers=sst.GEN_HEADERS
    )
    soup = bs(rsp.data.replace(b"\n", b""), "html.parser")
    teur= soup.find_all('table')[1]
    tusd = soup.find_all('table')[3]
    sup_entries = []
    for tr in teur.select('tbody tr'):
        dd, value, vv = map(lambda x: x['data-value'], tr.find_all('td'))
        dd = datetime.strptime(dd, '%Y-%m-%d').date()
        sup_entries.append([ dd, 'EUR', value, value ])
    for tr in tusd.select('tbody tr'):
        dd, value, vv = map(lambda x: x['data-value'], tr.find_all('td'))
        dd = datetime.strptime(dd, '%Y-%m-%d').date()
        sup_entries.append([ dd, 'USD', value, value ])
    entries = []
    for (odate, currency, buy, sale) in sup_entries:
        with db_clises() as ses:
            d = check_exchange_dup(
                    db = ses,
                    source = source,
                    currency = currency,
                    odate = odate,
                    buy = buy,
                    sales = sale
            )
            if not d:
                entries.append(
                    {
                        "group_source": group_source,
                        "source": source,
                        "currency": currency,
                        "sales": sale,
                        "buy": buy,
                        "year": odate.year,
                        "month": odate.month,
                        "date": odate,
                    }
                )
    if entries:
        with db_clises() as ses:
            ex_bulk_insert(ses, MODULE, MODEL, entries)

def familiarc_process(group_source: str):
    odate = date.today()
    source = 'FAMILIAR'
    curem = {
        'Dólar': 'USD',
        'Peso':  'ARS',
        'Real': 'BRL',
        'Euro': 'EUR'
    }
    rsp = htr.request('GET',
            sst.FAMILIAR,
            headers=sst.GEN_HEADERS
    )
    soup = bs(rsp.data.replace(b"\n", b""), "html.parser")
    entries = []
    for co in soup.find_all(class_='box-cotizacion'):
        cur = co.select('hgroup h3')[0].text
        ct = curem.get(cur)
        b,s = co.find_all('div')
        buy = b.find_all('p')[-1].text.replace('.', '').replace(',', '.')
        sale = s.find_all('p')[-1].text.replace('.', '').replace(',', '.')
        with db_clises() as ses:
            d = check_exchange_dup(
                    db = ses,
                    source = source,
                    currency = ct,
                    odate = odate,
                    buy = buy,
                    sales = sale
            )
            if not d:
                entries.append(
                    {
                        "group_source": group_source,
                        "source": source,
                        "currency": ct,
                        "sales": sale,
                        "buy": buy,
                        "year": odate.year,
                        "month": odate.month,
                        "date": odate,
                    }
                )
    if entries:
        with db_clises() as ses:
            ex_bulk_insert(ses, MODULE, MODEL, entries)

def setc_process(group_source: str):
    source = 'SET'
    months = {
        'Abril': '04',
        'Agosto': '08',
        'Diciembre': '12',
        'Enero': '01',
        'Febrero': '02',
        'Julio': '07',
        'Junio': '06',
        'Marzo': '03',
        'Mayo': '05',
        'Noviembre': '11',
        'Octubre': '10',
        'Septiembre': '09',
        'Setiembre': '09'
    }

    rsp = htr.request('GET',
            sst.SET,
            headers=sst.GEN_HEADERS
    )
    soup = bs(rsp.data.replace(b"\n", b""), "html.parser")
    sup_entries = []
    for ff in soup.find_all(class_='journal-content-article'):
        month, year = ff['data-analytics-asset-title'].replace('Tipos de cambios del mes de ', '').split()
        month = months.get(month)
        trs = ff.select('tbody tr')
        for tr in trs:
            tds = tr.find_all('td')
            if not tds: continue
            day, \
            usd_buy, usd_sales, \
            brl_buy, brl_sales, \
            ars_buy, ars_sales, \
            jpy_buy, jpy_sales, \
            eur_buy, eur_sales, \
            gbp_buy, gbp_sales = map(lambda x: x.text, tds)
            mms = [usd_buy, usd_sales,brl_buy, brl_sales,
                ars_buy, ars_sales,jpy_buy, jpy_sales,
                eur_buy, eur_sales,gbp_buy, gbp_sales]
            usd_buy, usd_sales, \
            brl_buy, brl_sales, \
            ars_buy, ars_sales, \
            jpy_buy, jpy_sales, \
            eur_buy, eur_sales, \
            gbp_buy, gbp_sales = map(lambda x: float(x.replace('.', '').replace(',', '.')), mms)
            odate = datetime.strptime(f'{year}{month}{day}', '%Y%m%d').date()
            sup_entries.append([ odate, 'USD', usd_buy, usd_sales ])
            sup_entries.append([ odate, 'BRL', brl_buy, brl_sales ])
            sup_entries.append([ odate, 'ARS', ars_buy, ars_sales ])
            sup_entries.append([ odate, 'JPY', jpy_buy, jpy_sales ])
            sup_entries.append([ odate, 'EUR', eur_buy, eur_sales ])
            sup_entries.append([ odate, 'GBP', gbp_buy, gbp_sales ])
    entries = []
    for (odate, 
         currency, 
         buy, 
         sale) in sup_entries:
        with db_clises() as ses:
            d = check_exchange_dup(
                    db = ses,
                    source = source,
                    currency = currency,
                    odate = odate,
                    buy = buy,
                    sales = sale
            )
            if not d:
                entries.append(
                    {
                        "group_source": group_source,
                        "source": source,
                        "currency": currency,
                        "sales": sale,
                        "buy": buy,
                        "year": odate.year,
                        "month": odate.month,
                        "date": odate,
                    }
                )
    if entries:
        with db_clises() as ses:
            ex_bulk_insert(ses, MODULE, MODEL, entries)

def lamoneda_process(group_source: str):
    odate = date.today()
    source = 'LAMONEDA'
    sources = [
        f'{source}_MATRIZ',
        f'{source}_JEBAI',
        f'{source}_CENTRO',
        f'{source}_SOL',
        f'{source}_SANBLAS',
    ]
    currency = {
        'EURO x GUARANI':'EUR', 
        'DOLAR x GUARANI': 'USD', 
        # 'DOLAR x PESOS', 
        # 'DOLAR INUSUAL x GUARANI', 
        # 'DOLAR x EURO', 
        'PESOS x GUARANI': 'ARS', 
        'REAL x GUARANI': 'BRL', 
        # 'DOLAR x REAL'
    }

    rsp = htr.request('GET',
            sst.LAMONEDA,
            headers=sst.GEN_HEADERS
    )
    soup = bs(rsp.data.replace(b"\n", b""), "html.parser")
    entries = []
    for (source, t) in zip(sources, soup.find_all('table')):
        for tr in t.select('tbody tr'):
            ii, cur, buy, sale = map(lambda x: x.text, tr.find_all('td'))
            curc = currency.get(cur.strip())
            if not curc: continue
            buy = float(buy.replace('.', '').replace(',', '.'))
            sale = float(sale.replace('.', '').replace(',', '.'))
            with db_clises() as ses:
                d = check_exchange_dup(
                        db = ses,
                        source = source,
                        currency = curc,
                        odate = odate,
                        buy = buy,
                        sales = sale
                )
                if not d:
                    entries.append(
                        {
                            "group_source": group_source,
                            "source": source,
                            "currency": curc,
                            "sales": sale,
                            "buy": buy,
                            "year": odate.year,
                            "month": odate.month,
                            "date": odate,
                        }
                    )
    if entries:
        with db_clises() as ses:
            ex_bulk_insert(ses, MODULE, MODEL, entries)

def bonanzac_process(group_source: str):
    odate = date.today()
    source = "BONANZA"
    curre = 'USD'
    rsp = htr.request('GET',
            sst.BONANZA,
            headers=sst.GEN_HEADERS
    )
    year = odate.year
    rd = rsp.data.replace(b'\n', b'').replace(b' ', b'').strip()
    exchanges = json.loads(re.findall(b"my_2d=(\[\[.*?\]\])", rd)[0])
    entries = []
    for (dd, sale, buy, curren) in exchanges:
        odate = datetime.strptime(f'{dd[:2]}{dd[2:].capitalize()}{year}','%d%b%Y')
        with db_clises() as ses:
            d = check_exchange_dup(
                    db = ses,
                    source = source,
                    currency = curre,
                    odate = odate,
                    buy = buy,
                    sales = sale
            )
            if not d:
                entries.append(
                    {
                        "group_source": group_source,
                        "source": source,
                        "currency": curre,
                        "sales": sale,
                        "buy": buy,
                        "year": odate.year,
                        "month": odate.month,
                        "date": odate,
                    }
                )
    if entries:
        with db_clises() as ses:
            ex_bulk_insert(ses, MODULE, MODEL, entries)

def visionc_process(group_source: str):
    curmap = {
        'DOLARES': 'USD',
        'REAL BRASILEÑO': 'BRL',
        'PESO ARGENTINO': 'ARS',
        'EUROS': 'EUR',
    }


    odate = date.today()
    source = "VISION"
    rsp = htr.request('GET',
            sst.VISIONC,
            headers=sst.GEN_HEADERS
    )
    soup = bs(rsp.data.replace(b"\n", b""), "html.parser")
    table = soup.find_all("table")[0]
    currens = map(lambda x: x.text, table.find_all(class_='text-bold--small'))
    currens = list(map(lambda x: curmap.get(x), currens))
    exchan = list(map(lambda x: x.text, table.find_all(class_="text-light--medium")))
    cc = map(lambda x: float(x[1].replace('.', '')), 
             filter(lambda x: x[0] % 2 == 0, enumerate(exchan)))
    vv = map(lambda x: float(x[1].replace('.', '')), 
             filter(lambda x: x[0] % 2 != 0, enumerate(exchan)))
    entries = []
    for (currency, buy, sale) in zip(currens, cc, vv):
        with db_clises() as ses:
            d = check_exchange_dup(
                    db = ses,
                    source = source,
                    currency = currency,
                    odate = odate,
                    buy = buy,
                    sales = sale
            )
            if not d:
                entries.append(
                    {
                        "group_source": group_source,
                        "source": source,
                        "currency": currency,
                        "sales": sale,
                        "buy": buy,
                        "year": odate.year,
                        "month": odate.month,
                        "date": odate,
                    }
                )
    if entries:
        with db_clises() as ses:
            ex_bulk_insert(ses, MODULE, MODEL, entries)

def mundialc_process(group_source: str):
    odate = date.today()
    source = "MUNDIAL_CAMBIOS"
    rsp = htr.request('GET', 
            sst.MUNDIALC,
            headers=sst.GEN_HEADERS
    )
    soup = bs(rsp.data.replace(b"\n", b""), "html.parser")
    cards = soup.find_all("div", class_="card")
    dexc = cards[0]
    currens = map(lambda x: x.text, dexc.find_all('h3', class_="titulo-divisa"))
    exchan = list(map(lambda x: x.text, dexc.find_all('h3', class_="divisa")))
    cc = map(lambda x: float(x[1].replace('.', '')), 
             filter(lambda x: x[0] % 2 == 0, enumerate(exchan)))
    vv = map(lambda x: float(x[1].replace('.', '')), 
             filter(lambda x: x[0] % 2 != 0, enumerate(exchan)))
    entries = []
    for (currency, buy, sale) in zip(currens, cc, vv):
        with db_clises() as ses:
            d = check_exchange_dup(
                    db = ses,
                    source = source,
                    currency = currency,
                    odate = odate,
                    buy = buy,
                    sales = sale
            )
            if not d:
                entries.append(
                    {
                        "group_source": group_source,
                        "source": source,
                        "currency": currency,
                        "sales": sale,
                        "buy": buy,
                        "year": odate.year,
                        "month": odate.month,
                        "date": odate,
                    }
                )
    if entries:
        with db_clises() as ses:
            ex_bulk_insert(ses, MODULE, MODEL, entries)

def eurocambios_process(group_source:str, currency: str, stab: str):
    cc = {
     'PYG': 'GS',
     'USD': 'US',
     'EUR': 'EU',
     'ARS': 'PA',
     'BRL': 'RS',
     'CLP': 'PC',
     'UYU': 'PU',
     'JPY': 'YE',
     'CAD': 'DC',
     'CHF': 'FS',
     'GBP': 'LE',
     'BOB': 'PB',
    }
    year = date.today().year
    source = f'EUROC_{stab}'
    pps = {'param': 'getGraficaUltimoMes',
           'moneda': cc.get(currency),
           'sucursal': stab
    }
    rsp = htr.request('GET', 
            sst.EUROC,
            fields=pps,
            headers=sst.GEN_HEADERS
    )
    dd = rsp.json()
    dates = dd[0]
    buys =[]
    sales = []
    for t in dd[1]:
        if t.get('label') == 'Compra':
            buys.extend(t.get('data'))
        if t.get('label') == 'Venta':
            sales.extend(t.get('data'))
    dates = map(lambda x: datetime.strptime(f'{x}/{year}', '%d/%m/%Y'), dates)
    buys = map(float, buys)
    sales = map(float, sales)
    entries = []
    for (ed, buy, sale) in zip(dates, buys, sales):
        with db_clises() as ses:
            d = check_exchange_dup(
                    db = ses,
                    source = source,
                    currency = currency,
                    odate = ed,
                    buy = buy,
                    sales = sale
            )
            if not d:
                entries.append(
                    {
                        "group_source": group_source,
                        "source": source,
                        "currency": currency,
                        "sales": sale,
                        "buy": buy,
                        "year": ed.year,
                        "month": ed.month,
                        "date": ed,
                    }
                )
    if entries:
        with db_clises() as ses:
            ex_bulk_insert(ses, MODULE, MODEL, entries)

def gnb_process(group_source: str):
    rsp = htr.request('GET', 
            sst.GNB,
            headers=sst.GEN_HEADERS
    )
    dd = rsp.json()
    source = 'GNB'
    entries = []
    ed = date.today()
    for dex in dd.get('exchangeRates'):
        currency = dex.get('currencyCode')
        buy = float(dex.get('cashBuyPrice'))
        sales = float(dex.get('cashSellPrice'))
        if (buy == 0) and (sales == 0): continue
        with db_clises() as ses:
            d = check_exchange_dup(
                    db = ses,
                    source = source,
                    currency = currency,
                    odate = ed,
                    buy = buy,
                    sales = sales
            )
            if not d:
                entries.append(
                    {
                        "group_source": group_source,
                        "source": source,
                        "currency": currency,
                        "sales": sales,
                        "buy": buy,
                        "year": ed.year,
                        "month": ed.month,
                        "date": ed,
                    }
                )
    if entries:
        with db_clises() as ses:
            ex_bulk_insert(ses, MODULE, MODEL, entries)

def myd_process(group_source: str):
    rsp = htr.request('GET', 
            sst.MYD,
            headers=sst.GEN_HEADERS
    )
    soup = bs(rsp.data.replace(b"\n", b""), "html.parser")
    cba = soup.find_all("div", class_="cambios-banner-text scrollbox")
    call = myd_subprocess(cba[0], 'MYD_ASU')
    ccde = myd_subprocess(cba[1], 'MYD_CDE')
    call.extend(ccde)
    entries = []
    for ex in call:
        with db_clises() as ses:
            ed =  ex.get('odate')
            d = check_exchange_dup(
                    db = ses,
                    source = ex.get('source'),
                    currency = ex.get('currency'),
                    odate = ed,
                    buy = ex.get('buy'),
                    sales = ex.get('sales')
            )
            if not d:
                entries.append(
                    {
                        "group_source": group_source,
                        "source": ex.get('source'),
                        "currency": ex.get('currency'),
                        "sales": ex.get('sales'),
                        "buy": ex.get('buy'),
                        "year": ed.year,
                        "month": ed.month,
                        "date": ed,
                    }
                )
    if entries:
        with db_clises() as ses:
            ex_bulk_insert(ses, MODULE, MODEL, entries)

def myd_subprocess(cc: list, source: str):
    currencies = {
       'us-1.png': 'USD',
       '640px-Flag_of_Europe.svg.png': 'EUR',
       'descarga.png': 'BRL',
       'ar.png': 'ARS',
       'cl[1].png': 'CLP',
       '200px-Flag_of_Uruguay_(1828-1830).svg.png': 'UYU',
       '260px-Bandera-de-inglaterra-400x240.png': 'GBP',
       'ca[2].png':'CAD',
       '175-suiza_400px[1].jpg':'CHF',
       'jp[1].png': 'JPY',
    }    
    edata = []
    for ul in cc.find_all('ul')[1:]:
        tt = {'odate': date.today(), 'source': source }
        for idx, li in enumerate(ul.find_all('li')):
            if idx == 0:
                img = li.find_all('img')
                if img:
                    cimg = img[0]['src'].split('/')[-1]
                    currency = currencies.get(cimg)
                    if not currency: continue
                    tt['currency'] = currency
            if idx == 1:
                tt['buy'] = li.text
            if idx == 2:
                tt['sales'] = li.text
        if tt.get('currency'):
            edata.append(tt)
    return edata

def alberdi_process(group_source: str):
    rsp = htr.request('GET', 
            sst.CA,
            headers=sst.GEN_HEADERS
    )
    dd = rsp.json()
    entries = []
    for (source, dex) in dd.items():
        source = f'ALBERDI_{source.upper()}'
        timer = dex.pop()
        ed = datetime.strptime(timer.get('compra'), '%d/%m/%Y')
        for e in dex:
            currency = e.get('bcp')
            buy = float(e.get('compra').replace('.', '').replace(',', '.'))
            sales = float(e.get('venta').replace('.', '').replace(',', '.'))
            if (buy == 0) and (sales == 0): continue
            with db_clises() as ses:
                d = check_exchange_dup(
                        db = ses,
                        source = source,
                        currency = currency,
                        odate = ed,
                        buy = buy,
                        sales = sales
                )
                if not d:
                    entries.append(
                        {
                            "group_source": group_source,
                            "source": source,
                            "currency": currency,
                            "sales": sales,
                            "buy": buy,
                            "year": ed.year,
                            "month": ed.month,
                            "date": ed,
                        }
                    )
        if entries:
            with db_clises() as ses:
                ex_bulk_insert(ses, MODULE, MODEL, entries)

        

def maxi_process(group_source: str, bdate: str, odate: str, currency: str):
    m_cur = {
        'USD': 'DÓLAR'
    }
    pps = { 
        "na": m_cur.get(currency, 'ND'), 
        "data_inicio": bdate, 
        "data_fin": odate
    }
    encoded_args = urlencode(pps)

    rsp = htr.request('POST', 
            sst.MAXI,
            body=encoded_args,
            headers=sst.MAX_HEADERS
    )
    rd = str(rsp.data).replace('\\n', '')\
            .replace('\\t', '')\
            .replace('\\\\', '')\
            .replace('\\', '')\
            .replace(' ', '').strip()
    tdates = re.findall("labels:\[(.*?)\]", 
                        rd.replace(' ', ''))[0]\
                            .replace('"', '')\
                            .replace('.', '')\
                            .strip(',').split(',')
    tdates = map(lambda x: datetime.strptime(x, '%d/%m/%y').date(), tdates)
    sales, buys = re.findall("data:\[(.*?)\]", rd.replace(' ', ''))
    sales = map(int , sales.replace('"', '').replace('.', '').strip(',').split(','))
    buys = map(int, buys.replace('"', '').replace('.', '').strip(',').split(','))
    entries = []
    for (ed, ss, bb)  in zip(tdates, sales, buys):
        with db_clises() as ses:
            d = check_exchange_dup(
                    db = ses,
                    source = 'MAXI',
                    currency = currency,
                    odate = ed,
                    buy = bb,
                    sales = ss
            )
            if not d:
                entries.append(
                    {
                        "group_source": group_source,
                        "source": "MAXI",
                        "currency": currency,
                        "sales": ss,
                        "buy": bb,
                        "year": ed.year,
                        "month": ed.month,
                        "date": ed,
                    }
                )
    if entries:
        with db_clises() as ses:
            ex_bulk_insert(ses, MODULE, MODEL, entries)
    return {'success': 'Done!!'}

def bcp_process(group_source: str, year: str, currency: str):
    rsp_buy = htr.request(
        "GET",
        sst.BCP,
        fields={"anho": year, "moneda": currency, "tipoOperacion": "compra"},
        headers=sst.GEN_HEADERS,
    )
    rsp_vta = htr.request(
        "GET",
        sst.BCP,
        fields={"anho": year, "moneda": currency, "tipoOperacion": "venta"},
        headers=sst.GEN_HEADERS,
    )
    # cotizacion-interbancaria
    bcp_excha = {}
    soup = bs(rsp_buy.data.replace(b"\n", b""), "html.parser")
    cta = soup.find_all(id="cotizacion-interbancaria")[-1]
    for tr in cta.find_all("tr")[1:]:
        day = tr.find_all("th")[0].get_text()
        for midx, m in enumerate(tr.find_all("td")):
            midx = str(midx + 1)
            odate = f"{year}-{midx.zfill(2)}-{day.zfill(2)}"
            ex = m.get_text()
            if ex == "ND":
                continue
            bcp_excha[odate] = {
                "buy": float(ex.replace(".", "").replace(",", ".")),
                "sales": 0,
            }
    
    soup = bs(rsp_vta.data.replace(b"\n", b""), "html.parser")
    cta = soup.find_all(id="cotizacion-interbancaria")[-1]
    for tr in cta.find_all("tr")[1:]:
        day = tr.find_all("th")[0].get_text()
        for midx, m in enumerate(tr.find_all("td")):
            midx = str(midx + 1)
            odate = f"{year}-{midx.zfill(2)}-{day.zfill(2)}"
            ex = m.get_text()
            if ex == "ND":
                continue
            if not bcp_excha.get(odate):
                bcp_excha[odate] = {"buy": 0}
            bcp_excha[odate].update(
                {"sales": float(ex.replace(".", "").replace(",", "."))}
            )
    entries = []
    for odate, exch in bcp_excha.items():
        odate = datetime.strptime(odate, '%Y-%m-%d')
        with db_clises() as ses:
            d = check_exchange_dup(
                    db = ses,
                    source = 'BCP',
                    currency = currency,
                    odate = odate,
                    buy = exch.get('buy'),
                    sales = exch.get('sales')
            )
            if not d:
                entries.append(
                    {
                        "group_source": group_source,
                        "source": "BCP",
                        "currency": currency,
                        "sales": exch.get('sales'),
                        "buy": exch.get('buy'),
                        "year": odate.year,
                        "month": odate.month,
                        "date": odate,
                    }
                )
    if entries:
        with db_clises() as ses:
            ex_bulk_insert(ses, MODULE, MODEL, entries)
    return {'success': 'Done!!'}            


def cc_process(group_source, currency):
    m_cur = {
        "PYG": "pyg",
        "USD": "usd",
        "BRL": "brl",
        "EUR": "eur",
        "CLP": "clp",
        "UYU": "uyu",
        "COP": "cop",
        "MXN": "mxn",
        "BOB": "bob",
        "PEN": "pen",
        "CAD": "cad",
        "AUD": "aud",
        "NOK": "nok",
        "DKK": "dkk",
        "SEK": "sek",
        "GBP": "gbp",
        "CHF": "chf",
        "JPY": "jpy",
        "KWD": "kwd",
        "ILS": "ils",
        "ZAR": "zar",
        "RUB": "rub",
    }
    logging.info(f"Get exchange data from {sst.CC}")
    rsp = htr.request(
        "GET", sst.CC, fields={"currency": m_cur.get(currency, 'ND')}, headers=sst.GEN_HEADERS
    )
    soup = bs(rsp.data.replace(b"\n", b""), "html.parser")
    cta = soup.find_all("table", class_="cotiz-tabla")
    inline_dups = set()
    for ht in cta:
        for tr in ht.tbody.find_all("tr"):
            dd = map(
                lambda x: x.get_text().replace(".", "").replace(",", "."),
                tr.find_all("td"),
            )
            ftdate, buy, sales = dd
            keyu = f"{currency}{ftdate}{buy}{sales}"
            if keyu in inline_dups:
                continue
            odate = datetime.strptime(ftdate, "%d/%m/%Y").date()
            entries = []
            with db_clises() as ses:
                d = check_exchange_dup(
                        db = ses,
                        source = 'CC',
                        currency = currency,
                        odate = odate,
                        buy = buy,
                        sales = sales
                )
                inline_dups.add(keyu)
                if not d:
                    entries.append(
                        {
                            "group_source": group_source,
                            "source": "CC",
                            "currency": currency,
                            "sales": sales,
                            "buy": buy,
                            "year": odate.year,
                            "month": odate.month,
                            "date": odate,
                        }
                    )
            if entries:
                with db_clises() as ses:
                    ex_bulk_insert(ses, MODULE, MODEL, entries)
    return {'success': 'Done!!'}


def check_exchange_dup(
            db: Session,
            source: str,
            currency: str,
            odate: date,
            buy: str | float,
            sales: str | float):
    d = ex_query(
        db,
        MODULE,
        MODEL,
        [
            {"attr": "currency", "optr": "==", "value": currency},
            {"attr": "source", "optr": "==", "value": source},
            {
                "attr": "date",
                "optr": "==",
                "value": odate.strftime("%Y-%m-%d"),
            },
            {"attr": "buy", "optr": "==", "value": buy},
            {"attr": "sales", "optr": "==", "value": sales},
        ],
        robj="scalar_one_or_none",
    )
    return d
