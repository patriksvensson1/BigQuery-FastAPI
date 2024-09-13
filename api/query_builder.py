from api.url_parameters import StocksParameters, PricesParameters
from google.cloud import bigquery
import api.config as config


async def prices_query(parameters: PricesParameters):
    query = f'''SELECT date, time, name, ticker, currency, current_price, high_price, low_price,
                open_price, previous_close_price, price_change, price_change_perc
                FROM {config.BQ_DATASET}.{config.BQ_TABLE}
                WHERE 1=1'''
    query_parameters = []

    if parameters.name:
        query += f' AND name = @name'
        query_parameters.append(bigquery.ScalarQueryParameter("name", "STRING", parameters.name))
    if parameters.ticker:
        query += f' AND ticker = @ticker'
        query_parameters.append(bigquery.ScalarQueryParameter("ticker", "STRING", parameters.ticker))
    if parameters.currency:
        query += f' AND currency = @currency'
        query_parameters.append(bigquery.ScalarQueryParameter("currency", "STRING", parameters.currency))
    if parameters.at_date:
        query += f' AND date = @at_date'
        query_parameters.append(bigquery.ScalarQueryParameter("at_date", "DATE", parameters.at_date))
    if parameters.from_date:
        query += f' AND date >= @from_date'
        query_parameters.append(bigquery.ScalarQueryParameter("from_date", "DATE", parameters.from_date))
    if parameters.to_date:
        query += f' AND date <= @to_date'
        query_parameters.append(bigquery.ScalarQueryParameter("to_date", "DATE", parameters.to_date))
    if parameters.at_time:
        query += f' AND time = @at_time'
        query_parameters.append(bigquery.ScalarQueryParameter("at_time", "TIME", str(parameters.at_time)))
    if parameters.from_time:
        query += f' AND time >= @from_time'
        query_parameters.append(bigquery.ScalarQueryParameter("from_time", "TIME", str(parameters.from_time)))
    if parameters.to_time:
        query += f' AND time <= @to_time'
        query_parameters.append(bigquery.ScalarQueryParameter("to_time", "TIME", str(parameters.to_time)))
    query += f' ORDER BY date, time, name'
    return query, query_parameters


async def stocks_query(parameters: StocksParameters):
    query = f'''SELECT date, time, name, ticker, industry, exchange, country, currency
                    FROM {config.BQ_DATASET}.{config.BQ_TABLE}
                    WHERE 1=1'''
    query_parameters = []

    if parameters.ticker:
        query += f' AND ticker = @ticker'
        query_parameters.append(bigquery.ScalarQueryParameter("ticker", "STRING", parameters.ticker))
    if parameters.industry:
        query += f' AND industry = @industry'
        query_parameters.append(bigquery.ScalarQueryParameter("industry", "STRING", parameters.industry))
    if parameters.exchange:
        query += f' AND exchange = @exchange'
        query_parameters.append(bigquery.ScalarQueryParameter("exchange", "STRING", parameters.exchange))
    query += f' ORDER BY date, time, name'
    return query, query_parameters
