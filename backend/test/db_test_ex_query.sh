#!/bin/bash
python ./test/db_opts.py --test_ex_query \
        --module "models.m_finance" \
        --model "Exchange" \
        --criteria '[ {"attr": "year", "optr": "==", "value": 2011 }, {"attr": "date", "optr": "==", "value": "2011-03-01"},{"attr": "source", "optr": "==", "value": "CC"}, {"attr": "buy", "optr": "==", "value": "213584.4646854441"} ]' \
        --type_scalar "scalar_one_or_none"