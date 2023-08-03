-- SQLite

SELECT source, sales, buy, (sales+buy)/2 as eavg FROM m_finance_exchange where date = '2023-07-31' and currency = 'USD' order by buy desc;

SELECT distinct(source) FROM m_finance_exchange 

SELECT distinct(group_source) FROM m_finance_exchange 

select * from m_finance_exchange where group_source is null

select * from m_finance_exchange where currency in ("USD -> BRL",
    "USD -> EUR",
    "USD -> ARS",
    "USD CHE -> BRL")

SELECT * FROM m_finance_exchange WHERE source = 'YRENDAGUE' AND year = 2023 and month = 5 order by date

DELETE FROM m_finance_exchange WHERE group_source = 'BCP';

DELETE FROM m_finance_exchange

SELECT * FROM m_finance_exchange WHERE group_source like 'alberdi';

SELECT m_finance_exchange.source,
       m_finance_exchange.currency,
       m_finance_exchange.sales, 
       m_finance_exchange.buy,
       m_finance_exchange.year,
       m_finance_exchange.month,
       m_finance_exchange.date,
p       m_finance_exchange.id,
       m_finance_exchange.created_at
FROM m_finance_exchange
WHERE EXTRACT("year" FROM m_finance_exchange.year) = 2023'
    AND m_finance_exchange.date = '2011-03-01'
    AND m_finance_exchange.source = 'CC'
    AND m_finance_exchange.buy = 213584.4646854441

