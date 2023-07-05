#!/bin/bash
curl -X 'POST' \
  'http://127.0.0.1:8000/1/retrieve/qs_execute?module=models.m_finance&model=Exchange&autocommit=true' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "attr": "source",
    "optr": "==",
    "value": "SET"
  },
  {
    "attr": "date",
    "optr": "between",
    "value": ["2020-01-01", "2023-01-01"]
  }
]'