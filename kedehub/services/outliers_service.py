import pandas as pd
from kedehub_client import get_sync_apis
from kedehub_client.exceptions import UnexpectedResponse
import time

def find_outliers(person):
    json = get_sync_apis().outliers_api.get_outliers(person)
    df = pd.read_json(json, orient='split')
    if not df.empty:
        df.set_index('commit_time', inplace=True)
        df.index = pd.to_datetime(df.index)
    return df

def update_outliers(person):
    try:
        status = get_sync_apis().outliers_api.auto_update_outliers(person)
        return status
    except UnexpectedResponse:
        time.sleep(35)
        return 0