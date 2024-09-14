import asyncio
from fastapi import FastAPI, Depends, HTTPException
from api.url_parameters import StocksParameters, PricesParameters
import api.query_builder as query_builder
import api.bigquery_client as bigquery_client
import api_key_gen.key_database as key_db

app = FastAPI()


@app.get('/')
async def root_method():
    return {'Placeholder': 'Temporary placeholder still'}


@app.get('/prices')     # something.something/prices
async def get_prices(parameters: PricesParameters = Depends()):
    if not parameters.key or not await check_key_exists(parameters.key):
        raise HTTPException(status_code=401, detail=f"Invalid API key.")
    try:
        key_db.update_last_used(parameters.key)
        query, query_parameters = await (query_builder.prices_query(parameters))
        query_result = await bigquery_client.execute_query(query, query_parameters)

        prices = [dict(row) for row in query_result]
        return prices
    except Exception as e:
        return {'Error': e}


@app.get('/stocks')     # something.something/stocks
async def get_stocks(parameters: StocksParameters = Depends()):
    if not parameters.key or not await check_key_exists(parameters.key):
        raise HTTPException(status_code=401, detail=f"Invalid API key.")
    try:
        key_db.update_last_used(parameters.key)
        query, query_parameters = await (query_builder.stocks_query(parameters))
        query_result = await bigquery_client.execute_query(query, query_parameters)

        prices = [dict(row) for row in query_result]
        return prices
    except Exception as e:
        return {'Error': e}


async def check_key_exists(api_key):
    return await asyncio.to_thread(key_db.key_exists, api_key)
