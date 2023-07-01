import logging
import argparse
import os, shutil
from sts import settings as sst
from g_exchanges import m_exchange

FP = os.path.realpath(os.path.curdir)

logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(name)s %(message)s',
            filename=f'{FP}/log/coti_set.log',
            filemode='w'
        )

parser = argparse.ArgumentParser(description='Scrap data from exchanges sites.')
parser.add_argument('--crawler_exchange', 
                    dest='crawler_exchange', 
                    nargs='?',
                    help='Craw exchange data'
                    )
parser.add_argument('--currency', 
                    dest='currency', 
                    nargs='?',
                    help='Which currency to get'
                    )
parser.add_argument('--stab', 
                    dest='stab', 
                    nargs='?',
                    help='From which stablishment get the exchange'
                    )
parser.add_argument('--odate', 
                    dest='odate', 
                    nargs='?',
                    help='Which date to get'
                    )

parser.add_argument('--bdate', 
                    dest='bdate', 
                    nargs='?',
                    help='From which date to get'
                    )

parser.add_argument('--year', 
                    dest='year', 
                    nargs='?',
                    help='Which year to get'
                    )
parser.add_argument('--month', 
                    dest='month', 
                    nargs='?',
                    help='Which month to get'
                    )
parser.add_argument('--init_alembic', 
                    dest='init_alembic', 
                    action='store_true',
                    help='Initialize alembic configuration'
                    )

args = parser.parse_args()
if args.crawler_exchange:
    group_source = args.crawler_exchange.lower()
    if group_source  == 'cambios_chaco':
        m_exchange.cc_process(group_source,args.currency)
    if group_source  == 'bcp':
        m_exchange.bcp_process(group_source,args.year, args.currency)
    if group_source  == 'maxi':
        m_exchange.maxi_process(group_source,args.bdate, args.odate, args.currency)
    if group_source  == 'alberdi':
        m_exchange.alberdi_process(group_source)
    if group_source  == 'myd':
        m_exchange.myd_process(group_source)
    if group_source  == 'gnb':
        m_exchange.gnb_process(group_source)
    if group_source  == 'euroc':
        m_exchange.eurocambios_process(group_source,args.currency, args.stab)
    if group_source  == 'mundialc':
        m_exchange.mundialc_process(group_source)
    if group_source  == 'visionc':
        m_exchange.visionc_process(group_source)
    if group_source  == 'bonanza':
        m_exchange.bonanzac_process(group_source)
    if group_source  == 'lamoneda':
        m_exchange.lamoneda_process(group_source)
    if group_source  == 'set':
        m_exchange.setc_process(group_source)
    if group_source  == 'familiar':
        m_exchange.familiarc_process(group_source)
    if group_source  == 'expansion':
        m_exchange.expansion_process(group_source,args.year, args.month)
    if group_source  == 'yrendague':
        m_exchange.yrendague_process(group_source,args.bdate, args.odate, args.currency)
    if group_source  == 'triplec':
        m_exchange.triplec_process(group_source,args.year, args.month)

if args.init_alembic:
    import sys
    mdirs = [
        f'{FP}/alembic/versions/',
        f'{FP}/alembic/versions/__pycache__/',
    ]
    for mdir in mdirs:
        try:
            shutil.rmtree(mdir)
        except Exception as e:
            logging.info(f'Error removing migration folder {e}')
        else:
            logging.info(f'Successfully removing folder {mdir}')
        try:
            os.mkdir(mdir)
        except:
            pass
    try:
        os.remove(f'{FP}/{sst.DB_NAME}')
    except:
        pass
    sys.exit(0)
