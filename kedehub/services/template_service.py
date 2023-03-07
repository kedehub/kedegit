from kedehub_client import get_sync_apis


def save_templates(df,  person : str):
    json = df.to_json(orient='split')
    get_sync_apis().template_api.save_template(json,person)