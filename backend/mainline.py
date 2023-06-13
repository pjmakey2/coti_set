import logging
import argparse
import os, shutil
import asyncio
from sts import settings as sst
from g_exchanges import m_exchange_historic

FP = os.path.realpath(os.path.curdir)

logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(name)s %(message)s',
            filename=f'{FP}/log/coti_set.log',
            filemode='w'
        )

parser = argparse.ArgumentParser(description='Scrap data from exchanges sites.')
parser.add_argument('--historic', 
                    dest='historic', 
                    nargs='?',
                    help='Get historic exchange data'
                    )
parser.add_argument('--init_alembic', 
                    dest='init_alembic', 
                    action='store_true',
                    help='Initialize alembic configuration'
                    )

args = parser.parse_args()
if args.historic:
    if args.historic.lower()  == 'cambios_chaco':
        m_exchange_historic.cc_process(sst.HIST_CC)

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
