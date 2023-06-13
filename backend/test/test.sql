-- SQLite

SELECT m_finance_exchange.source,
       m_finance_exchange.currency,
       m_finance_exchange.sales,
       m_finance_exchange.buy,
       m_finance_exchange.year,
       m_finance_exchange.month,
       m_finance_exchange.date,
       m_finance_exchange.id,
       m_finance_exchange.created_at
FROM m_finance_exchange
WHERE EXTRACT("year" FROM m_finance_exchange.year) = 2023
    AND m_finance_exchange.date = '2011-03-01'
    AND m_finance_exchange.source = 'CC'
    AND m_finance_exchange.buy = 213584.4646854441