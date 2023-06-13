import logging, json, argparse, os, sys
from models.m_finance import Exchange, Base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, insert, select, func
from datetime import datetime
from random import choice, uniform
HOME = os.environ["HOME"]
PROJECT = f"/{HOME}/projects/coti_set/backend"
TEST_DIR = f"/{PROJECT}/test"
logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(name)s %(message)s',
            filename=f'{TEST_DIR}//coti_set_test.log',
            filemode='w'
        )

sys.path.append(PROJECT)
sqlitef = f"/{TEST_DIR}/test.sqlite"
from sts import settings as sst
#sst.SQLALCHEMY_DATABASE_URI = f"sqlite://{sqlitef}"
from db.uw_exchange import construct_criteria

def random_numeric_data(rr, start, end, ntype = float, unique: bool = False) -> list:
    logging.info(f'Generate {rr} of fake data from start {start} to end {end} of type {ntype} that is {unique} unique')
    dd = []
    for i in range(rr):
        dd.append(
            ntype(uniform(start, end))
            )
    if unique: return list(set(dd))
    return dd





parser = argparse.ArgumentParser(description='Scrap data from exchanges sites.')
parser.add_argument('--initialize_db',action='store_true',default=False,help='Remove and initialize the test atabase')
parser.add_argument('--populate_db',action='store_true',default=False,help='Populate the db with fake data')
parser.add_argument('--n_values',nargs='*',
                    type=int,
                    help='Range of random numbers', 
                    default=100)
parser.add_argument('--start_n_value',nargs='?',type=int,help='Starting point for the Range of random numbers', default=1)
parser.add_argument('--end_n_value',nargs='?',type=int,help='Ending point for the Range of random numbers', default=1000000)
parser.add_argument('--test_criteria_query',nargs='?',type=str,help='Receive a json string as an input')

args = parser.parse_args()

n_values = args.n_values
start_n_value = args.start_n_value
end_n_value = args.end_n_value

fake_numbers = random_numeric_data(n_values, start_n_value, end_n_value)

if args.initialize_db:
    logging.info(f'Removing {sqlitef}')
    try:
        os.remove(sqlitef)
    except:
        pass
    finally:
        logging.info(f'Create connection to {sqlitef}')
        engine = create_engine(sst.SQLALCHEMY_DATABASE_URI, echo=False)
        conn = engine.connect()
        Base.metadata.create_all(engine)

if args.populate_db:
    engine = create_engine(sst.SQLALCHEMY_DATABASE_URI, echo=False)
    engine.connect()
    data = []
    fake_year = random_numeric_data(10, 
                        2000, 
                        2000+50, 
                        ntype=int)
    fake_month = range(1, 13)
    logging.info(f'Creating {n_values} fake records')
    for a in range(1, n_values):
        fy = choice(fake_year)
        fm = choice(fake_month)
        data.append(
            {
                "source": choice(["SET", "BCP", "CC", "SANTA RITA", "DOMINIC TORETTO"]),
                "currency": "PYG",
                "sales": choice(fake_numbers),
                "buy": choice(fake_numbers),
                "year": fy,
                "month": fm,
                "date": datetime.strptime(f'{fy}-{str(fm).zfill(2)}-01', '%Y-%m-%d'),
            }
        )
    with Session(engine) as session:
        session.execute(
            insert(Exchange),
            data
        )
        session.commit()
        rsp = session.query(func.count(Exchange.id)).scalar()
        logging.info(f'There is {rsp} records in the data for model Exchange')
if args.test_criteria_query:
    engine = create_engine(sst.SQLALCHEMY_DATABASE_URI, echo=False)
    engine.connect()    
    criteria = json.loads(args.test_criteria_query)
    qcrt = construct_criteria('models.m_finance', 'Exchange', criteria)
    stmt = select(Exchange).where(*qcrt)
    stcm = stmt.compile(compile_kwargs={"literal_binds": True})
    logging.info(f'Testing constructing of criteria by json {stcm}')
    with Session(engine) as session:
        logging.info(f'Executed {stmt} against model current engine')
        for d in session.execute(stmt).scalars():
            ddi = d.__dict__
            ddi.pop('_sa_instance_state', None)
            print(ddi)
