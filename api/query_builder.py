from api.api_parameters import StocksParameters, PricesParameters
import api.config as config


async def all_data_query():
    query = f'''SELECT * FROM {config.BQ_DATASET}.{config.BQ_TABLE}
        ORDER BY date, time, name'''
    return {'Query': query}


async def prices_query(parameters: PricesParameters):
    query = f'''SELECT date, time, name, ticker, currency, current_price, high_price, low_price,
                open_price, previous_close_price, price_change, price_change_perc
                FROM {config.BQ_DATASET}.{config.BQ_TABLE}
                WHERE 1=1'''
    if parameters.ticker:
        query += f' AND ticker = {parameters.ticker}'
    if parameters.date:
        query += f' AND date = {parameters.date}'
    if parameters.from_date:
        query += f' AND date >= {parameters.from_date}'
    if parameters.to_date:
        query += f' AND date <= {parameters.to_date}'
    if parameters.time:
        query += f' AND time = {parameters.time}'
    if parameters.from_time:
        query += f' AND time >= {parameters.from_time}'
    if parameters.to_time:
        query += f' AND time <= {parameters.to_time}'
    query += f' ORDER BY date, time, name'
    return query


async def stocks_query(parameters: StocksParameters):
    query = f'''SELECT date, time, name, ticker, industry, exchange, country, currency
                    FROM {config.BQ_DATASET}.{config.BQ_TABLE}
                    WHERE 1=1'''
    if parameters.ticker:
        query += f' AND ticker = {parameters.ticker}'
    if parameters.industry:
        query += f' AND industry = {parameters.industry}'
    if parameters.exchange:
        query += f' AND exchange >= {parameters.exchange}'
    query += f' ORDER BY date, time, name'
    return query
