from fastapi import HTTPException
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest
import config.config as config


client = bigquery.Client(credentials=config.CREDENTIALS)


async def execute_query(query, query_parameters):
    try:
        job_config = bigquery.QueryJobConfig(query_parameters=query_parameters)
        query_job = client.query(query, job_config=job_config)
        return query_job.result()
    except BadRequest as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
