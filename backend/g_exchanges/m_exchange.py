from datetime import datetime
import urllib3 as htr, json, logging
from bs4 import BeautifulSoup as bs
from db.g_session import db_clises
from db.uw_exchange import ex_query, ex_bulk_insert
from sts import settings as sst

MODULE = "models.m_finance"
MODEL = "Exchange"


def bcp_process(fecha: str):
    http = htr.PoolManager(
        cert_reqs = "CERT_NONE"
    )
    print(sst.BCP, 'beging', fecha)
    rsp = htr.request(
        "GET", sst.BCP, fields={"fecha": fecha}, headers=sst.HEADERS,
    )
    print(sst.BCP, 'END', fecha)
    soup = bs(rsp.data.replace(b"\n", b""), "html.parser")
    with open('/tmp/bcp.html', 'w') as ff:
        ff.write(soup.prettify())
    


def cc_process(currency):
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
        "GET", sst.CC, fields={"currency": m_cur.get(currency)}, headers=sst.HEADERS
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
            date, buy, sales = dd
            keyu = f"{currency}{date}{buy}{sales}"
            if keyu in inline_dups:
                continue
            odate = datetime.strptime(date, "%d/%m/%Y").date()
            entries = []
            with db_clises() as ses:
                d = ex_query(
                    ses,
                    MODULE,
                    MODEL,
                    [
                        {"attr": "currency", "optr": "==", "value": currency},
                        {"attr": "source", "optr": "==", "value": "CC"},
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
                inline_dups.add(keyu)
                if not d:
                    entries.append(
                        {
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
                print("Insert")
                with db_clises() as ses:
                    ex_bulk_insert(ses, MODULE, MODEL, entries)
