from datetime import datetime
import urllib3 as htr, json, logging
from bs4 import BeautifulSoup as bs

def cc_process(url):
    logging.info(f"Get historic data from {url}")
    rsp = htr.request("GET", url)
    soup = bs(rsp.data.replace(b'\n', b''), 'html.parser')
    cta = soup.find_all("table", class_="cotiz-tabla")
    for ht in cta:
        for tr in ht.tbody.find_all('tr'):
            dd = map(lambda x: x.get_text().replace('.', '').replace(',', '.'), 
                     tr.find_all('td'))
            date, buy, sell = dd
            date = datetime.strptime(date, '%d/%m/%Y')
            print(date, buy, sell, sep='\n')
