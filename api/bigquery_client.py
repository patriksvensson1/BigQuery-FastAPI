from google.cloud import bigquery
import api.config as config


async def execute_query(query):
    client = bigquery.Client(credentials=config.CREDENTIALS)
    query_job = client.query(query)
    return query_job.result()
