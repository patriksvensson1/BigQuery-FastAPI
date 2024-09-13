from fastapi.testclient import TestClient
from dotenv import load_dotenv
load_dotenv('test_variables.env')

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


def test_prices_one_str_parameter():
    response = test_client.get('/prices?ticker=HFI')
    result = response.json()
    assert response.status_code == 200
    assert len(result) == 1
    assert any(row.get('ticker') == 'HFI' for row in result)


def test_prices_multiple_str_parameters():
    response = test_client.get('/prices?name=Telecom Plus&currency=GBP')
    result = response.json()
    assert response.status_code == 200
    assert len(result) == 1
    assert any(row.get('name') == 'Telecom Plus' and row.get('currency') == 'GBP' for row in result)


def test_prices_one_date_parameter():
    response = test_client.get('/prices?at_date=2024-09-07')
    result = response.json()
    assert response.status_code == 200
    assert len(result) == 1
    assert any(row.get('date') == '2024-09-07' for row in result)


def test_prices_multiple_date_parameters():
    response = test_client.get('/prices?from_date=2024-09-07&to_date=2024-09-08')
    result = response.json()
    assert response.status_code == 200
    assert len(result) == 11
    assert any(row.get('date') == '2024-09-07' or row.get('date') == '2024-09-08' for row in result)


def test_stocks_one_str_parameter():
    response = test_client.get('/stocks?ticker=AGC')
    result = response.json()
    assert response.status_code == 200
    assert len(result) == 1
    assert any(row.get('ticker') == 'AGC' for row in result)


def test_stocks_multiple_str_parameters():
    response = test_client.get('/stocks?ticker=FNT&industry=Finance')
    result = response.json()
    assert response.status_code == 200
    assert len(result) == 1
    assert any(row.get('ticker') == 'FNT' and row.get('industry') == 'Finance' for row in result)


def test_prices_invalid_strings():
    invalid_strings = [
        'prices?name=INVALID_NAME',
        'prices?ticker=INVALID_TICKER',
        'prices?currency=INVALID_CURRENCY'
    ]
    for line in invalid_strings:
        response = test_client.get(line)
        result = response.json()
        assert response.status_code == 200
        assert len(result) == 0


def test_prices_invalid_date_and_time():
    invalid_date_and_time = [
        'prices?from_date=INVALID_DATE',
        'prices?to_date=INVALID_DATE',
        'prices?at_date=INVALID_DATE',
        'prices?from_time=INVALID_TIME',
        'prices?to_time=INVALID_TIME',
        'prices?at_time=INVALID_TIME'
    ]

    for line in invalid_date_and_time:
        response = test_client.get(line)
        result = response.json()
        assert response.status_code == 422  # Validation issues = 422
        assert "error" in result["detail"][0]["ctx"]


def test_stocks_invalid_strings():
    invalid_strings = [
        'stocks?ticker=INVALID_TICKER',
        'stocks?industry=INVALID_INDUSTRY',
        'stocks?exchange=INVALID_EXCHANGE'
    ]
    for line in invalid_strings:
        response = test_client.get(line)
        result = response.json()
        assert response.status_code == 200
        assert len(result) == 0


def test_sql_injections():
    injection_tests = [
        '/stocks?ticker=test\' OR 1=1',
        '/prices?ticker=test\' OR 1=1',
        '/stocks?ticker=test\' UNION 1,2',
        '/prices?ticker=test\' UNION 1,2'
    ]

    for url in injection_tests:
        response = test_client.get(url)
        result = response.json()
        assert response.status_code == 200
        assert len(result) == 0
