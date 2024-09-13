from fastapi import FastAPI, Depends
from api.url_parameters import StocksParameters, PricesParameters
import api.query_builder as query_builder
import api.bigquery_client as bigquery_client

app = FastAPI()


@app.get('/')
async def root_method():
    return {'Placeholder': 'Temporary placeholder still'}


@app.get('/prices')     # something.something/prices
async def get_prices(parameters: PricesParameters = Depends()):
    try:
        query, query_parameters = await (query_builder.prices_query(parameters))
        query_result = await bigquery_client.execute_query(query, query_parameters)

        prices = [dict(row) for row in query_result]
        return prices
    except Exception as e:
        return {'Error!': e}


@app.get('/stocks')     # something.something/stocks
async def get_stocks(parameters: StocksParameters = Depends()):
    try:
        query, query_parameters = await (query_builder.stocks_query(parameters))
        query_result = await bigquery_client.execute_query(query, query_parameters)

        prices = [dict(row) for row in query_result]
        return prices
    except Exception as e:
        return {'Error!': e}
