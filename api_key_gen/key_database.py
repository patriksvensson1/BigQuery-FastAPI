from google.cloud import firestore
from datetime import datetime
import config.config as config

database = firestore.Client(credentials=config.CREDENTIALS)


def key_exists(api_key):
    try:
        document_reference = database.collection('API_Key').document(api_key)
        document = document_reference.get()
        return document.exists
    except Exception as e:
        return {'Error!': e}


def add_key(api_key):
    try:
        data_to_add = {"key": api_key, "created_date": datetime.now(), "last_used": datetime.now()}
        database.collection('API_Key').document(api_key).set(data_to_add)
    except Exception as e:
        return {'Error!': e}


def update_last_used(api_key):
    try:
        api_key_reference = database.collection('API_Key').document(api_key)
        api_key_reference.update({"last_used": datetime.now()})
    except Exception as e:
        return {'Error': e}


def delete_key(api_key):
    try:
        database.collection("API_Key").document(api_key).delete()
    except Exception as e:
        return {'Error': e}
