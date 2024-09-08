from fastapi import FastAPI, Depends
from api.api_parameters import StocksParameters, PricesParameters
import api.query_builder as query_builder

app = FastAPI()


@app.get('/')
async def method():
    query = await (query_builder.all_data_query())
    return {'Placeholder query': query}


@app.get('/prices')     # something.something/prices
async def get_prices(parameters: PricesParameters = Depends()):
    query = await (query_builder.prices_query(parameters))
    return {'Placeholder query': query}


@app.get('/stocks')     # something.something/stocks
async def get_stocks(parameters: StocksParameters = Depends()):
    query = await (query_builder.stocks_query(parameters))
    return {'Placeholder query': query}

