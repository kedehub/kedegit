from kedehub_client import get_sync_apis

def calculate_rank(last_week, today):
    get_sync_apis().ranklist_api.post_calculate_ranklist(last_week, today)

def load_rank_for_people(people_to_show, start_date, end_date):
    return get_sync_apis().ranklist_api.load_ranklist(people_to_show, start_date, end_date)