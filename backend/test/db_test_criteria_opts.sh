#!/bin/bash
#Testing == operator
python ./test/db_opts.py --test_criteria \
            --criteria '[ {"attr": "source", "optr": "==", "value": "SET"} ]'
#Testing > operator
python ./test/db_opts.py --test_criteria \
            --criteria '[ {"attr": "buy", "optr": ">", "value": 1000} ]'
#Testing < operator
python ./test/db_opts.py --test_criteria \
            --criteria '[ {"attr": "sales", "optr": "<", "value": 4000} ]'
#Testing >= operator
python ./test/db_opts.py --test_criteria \
            --criteria '[ {"attr": "sales", "optr": ">=", "value": 4000} ]'
#Testing <= operator
python ./test/db_opts.py --test_criteria \
            --criteria '[ {"attr": "buy", "optr": "<=", "value": 10000} ]'
#Testing in operator
python ./test/db_opts.py --test_criteria \
            --criteria '[ {"attr": "source", "optr": "in", "value": ["SET", "BCP", "CC"]} ]'
python ./test/db_opts.py --test_criteria \
            --criteria '[ {"attr": "date", "optr": "in", "value": ["2045-01-01", "2023-07-12", "2021-02-28"]} ]'
#Testing extract functions
python ./test/db_opts.py --test_criteria \
            --criteria '[ {"attr": "date", "optr": "extract", "value": "2021", "extract_value": "year"} ]'
#Testing between operator
python ./test/db_opts.py --test_criteria \
            --criteria '[ {"attr": "date", "optr": "between", "value": ["2021-01-01", "2023-12-31"]} ]'