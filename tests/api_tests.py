from fastapi.testclient import TestClient
from api.main import app


test_client = TestClient(app)


def test_reach_root_endpoint():
    response = test_client.get('/')
    assert response.status_code == 200


def test_reach_prices_endpoint():
    response = test_client.get('/prices')
    assert response.status_code == 200


def test_reach_stock_endpoint():
    response = test_client.get('/stocks')
    assert response.status_code == 200


def test_prices_with_one_parameter():
    response = test_client.get('/prices?ticker=HFI')
    result = response.json()
    query = result['Placeholder query']
    assert response.status_code == 200
    assert ' AND ticker = test' in query


def test_prices_with_multiple_parameters():
    response = test_client.get('/prices?from_date=2024-09-07&to_date=2024-09-08')
    result = response.json()
    query = result['Placeholder query']
    assert response.status_code == 200
    assert ' AND date >= 2024-09-07 AND date <= 2024-09-08' in query


def test_stocks_with_one_parameter():
    response = test_client.get('/stocks?ticker=test')
    result = response.json()
    query = result['Placeholder query']
    assert response.status_code == 200
    assert ' AND ticker = test' in query


def test_stocks_with_multiple_parameters():
    response = test_client.get('/stocks?ticker=test&industry=example')
    result = response.json()
    query = result['Placeholder query']
    assert response.status_code == 200
    assert ' AND ticker = test AND industry = example' in query
