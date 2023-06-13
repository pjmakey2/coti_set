from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
import os, sys

HOME = os.environ["HOME"]
PROJECT = f"/{HOME}/projects/coti_set/backend"
sys.path.append(PROJECT)
from models.m_finance import Exchange, Base

sqlitef = f"/{PROJECT}/test/test.sqlite"
os.remove(sqlitef)

# Create an engine and connect to the database
engine = create_engine(f"sqlite://{sqlitef}", echo=False)


conn = engine.connect()
Base.metadata.create_all(engine)

from datetime import date
from decimal import Decimal

data = [
    Exchange(
        **{
            "source": "SET",
            "currency": "PYG",
            "sales": 1234.99,
            "buy": 1234.99,
            "year": 2023,
            "month": 7,
            "date": date.today(),
        }
    ),
    Exchange(
        **{
            "source": "SET",
            "currency": "PYG",
            "sales": 1234.99,
            "buy": 1234.99,
            "year": 2023,
            "month": 7,
            "date": date.today(),
        }
    ),
    Exchange(
        **{
            "source": "SET",
            "currency": "PYG",
            "sales": Decimal("1234.99"),
            "buy": Decimal("1234.99"),
            "year": 2023,
            "month": 7,
            "date": date.today(),
        }
    ),
]

with Session(engine) as session:
    session.add_all(data)
    session.commit()

# Selects
import json


with Session(engine) as session:
    z = select(Exchange).filter(Exchange.date == "2023-06-12")
    rsp = session.execute(z)
    for d in rsp.scalars():
        for r in range(10):
            print(f"Adding comment {r} to {d.id}")
            d.exchangedetail.append(ExchangeDetail(**{"description": f"comment{r}"}))
    session.commit()
z = select(ExchangeDetail)
rsp = session.execute(z)
for d in rsp.scalars():
    print(d)
# Get an object orm by ID
# z = select(Exchange).filter(Exchange.id == 1)
exchangeobj = session.get(Exchange, 1)
