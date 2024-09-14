import time
from fastapi.testclient import TestClient
from dotenv import load_dotenv
load_dotenv('test_variables.env')

from api.main import app
import api_key_gen.key_database as key_db

test_client = TestClient(app)


def test_add_new_api_key():
    key_db.add_key("Test_Key")
    assert key_db.key_exists("Test_Key")


def test_reach_root_endpoint():
    response = test_client.get('/')
    assert response.status_code == 200


def test_reach_prices_endpoint():
    response = test_client.get('/prices?key=Test_Key')
    assert response.status_code == 200


def test_reach_stock_endpoint():
    response = test_client.get('/stocks?key=Test_Key')
    assert response.status_code == 200


def test_prices_one_str_parameter():
    response = test_client.get('/prices?ticker=HFI&key=Test_Key')
    result = response.json()
    assert response.status_code == 200
    assert len(result) == 1
    assert any(row.get('ticker') == 'HFI' for row in result)


def test_prices_multiple_str_parameters():
    response = test_client.get('/prices?name=Telecom Plus&currency=GBP&key=Test_Key')
    result = response.json()
    assert response.status_code == 200
    assert len(result) == 1
    assert any(row.get('name') == 'Telecom Plus' and row.get('currency') == 'GBP' for row in result)


def test_prices_one_date_parameter():
    response = test_client.get('/prices?at_date=2024-09-07&key=Test_Key')
    result = response.json()
    assert response.status_code == 200
    assert len(result) == 1
    assert any(row.get('date') == '2024-09-07' for row in result)


def test_prices_multiple_date_parameters():
    response = test_client.get('/prices?from_date=2024-09-07&to_date=2024-09-08&key=Test_Key')
    result = response.json()
    assert response.status_code == 200
    assert len(result) == 11
    assert any(row.get('date') == '2024-09-07' or row.get('date') == '2024-09-08' for row in result)


def test_stocks_one_str_parameter():
    response = test_client.get('/stocks?ticker=AGC&key=Test_Key')
    result = response.json()
    assert response.status_code == 200
    assert len(result) == 1
    assert any(row.get('ticker') == 'AGC' for row in result)


def test_stocks_multiple_str_parameters():
    response = test_client.get('/stocks?ticker=FNT&industry=Finance&key=Test_Key')
    result = response.json()
    assert response.status_code == 200
    assert len(result) == 1
    assert any(row.get('ticker') == 'FNT' and row.get('industry') == 'Finance' for row in result)


def test_prices_invalid_strings():
    invalid_strings = [
        'prices?name=INVALID_NAME&key=Test_Key',
        'prices?ticker=INVALID_TICKER&key=Test_Key',
        'prices?currency=INVALID_CURRENCY&key=Test_Key'
    ]
    for line in invalid_strings:
        response = test_client.get(line)
        result = response.json()
        assert response.status_code == 200
        assert len(result) == 0


def test_prices_invalid_date_and_time():
    invalid_date_and_time = [
        'prices?from_date=INVALID_DATE&key=Test_Key',
        'prices?to_date=INVALID_DATE&key=Test_Key',
        'prices?at_date=INVALID_DATE&key=Test_Key',
        'prices?from_time=INVALID_TIME&key=Test_Key',
        'prices?to_time=INVALID_TIME&key=Test_Key',
        'prices?at_time=INVALID_TIME&key=Test_Key'
    ]

    for line in invalid_date_and_time:
        response = test_client.get(line)
        result = response.json()
        assert response.status_code == 422  # Validation issues = 422
        assert "error" in result["detail"][0]["ctx"]


def test_stocks_invalid_strings():
    invalid_strings = [
        'stocks?ticker=INVALID_TICKER&key=Test_Key',
        'stocks?industry=INVALID_INDUSTRY&key=Test_Key',
        'stocks?exchange=INVALID_EXCHANGE&key=Test_Key'
    ]
    for line in invalid_strings:
        response = test_client.get(line)
        result = response.json()
        assert response.status_code == 200
        assert len(result) == 0


def test_sql_injections():
    injection_tests = [
        '/stocks?key=Test_Key&ticker=test\' OR 1=1',
        '/prices?key=Test_Key&ticker=test\' OR 1=1',
        '/stocks?key=Test_Key&ticker=test\' UNION 1,2',
        '/prices?key=Test_Key&ticker=test\' UNION 1,2'
    ]

    for url in injection_tests:
        response = test_client.get(url)
        result = response.json()
        assert response.status_code == 200
        assert len(result) == 0


def test_update_api_key_last_used():
    doc_reference = key_db.database.collection("API_Key").document("Test_Key")
    document =  doc_reference.get()
    first_timestamp = document.get("last_used")

    time.sleep(1)   # 1 second
    key_db.update_last_used("Test_Key")

    doc_reference = key_db.database.collection("API_Key").document("Test_Key")
    document = doc_reference.get()
    second_timestamp = document.get("last_used")

    assert first_timestamp != second_timestamp


def test_delete_api_key():
    key_db.delete_key("Test_Key")
    doc_reference = key_db.database.collection("API_Key").document("Test_Key")
    document = doc_reference.get()

    assert not document.exists
