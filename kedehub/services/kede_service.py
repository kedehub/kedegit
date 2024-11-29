from io import StringIO

from kedehub_client import get_sync_apis
from kedehub_client.exceptions import UnexpectedResponse
import time
import pandas as pd

def calculate_kede_for_person(project, person):
    try:
        get_sync_apis().kedestats_api.post_calculate_kede_for_person(project, person)
    except UnexpectedResponse:
        time.sleep(35)

def calculate_weekly_kede_for_person(project, person):
    try:
        get_sync_apis().kedestats_api.post_calculate_weekly_kede_for_person(project, person)
    except UnexpectedResponse:
        time.sleep(35)

def find_wrongly_calculated_kede_stats_for_authors_repo_id(repository_id: int, kede_freq: str):
    json = get_sync_apis().kedestats_api.get_wrongly_calculated_kede_stats_for_authors_repo_id(repository_id, kede_freq)
    df = pd.read_json(StringIO(json), orient='split')
    if not df.empty:
        df.set_index('commit_date', inplace=True)
        df.index = pd.to_datetime(df.index)
    return df

def delete_kede_for_repo(repository_id):
    get_sync_apis().kedestats_api.delete_kede_for_repo(repository_id)