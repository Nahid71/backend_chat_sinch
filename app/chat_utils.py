import requests
from config import Settings

def create_conversation(app_id, contact_id):
    region = "us"
    url = "https://" + region + ".conversation.api.sinch.com/v1/projects/" + Settings.sinch_project_id + "/conversations"
    payload = {
    "active": True,
    "active_channel": "WHATSAPP",
    "app_id": "{app_id}",
    "contact_id": "{contact_id}",
    "id": "string",
    "metadata": "string",
    "metadata_json": {}
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers, auth=(Settings.sinch_key,Settings.sinch_secret))
    if response.status_code == 200:
        conversation_data = response.json()
        return conversation_data
    else:
        return "Something is wrong"

def list_conversation(app_id):
    region = "us"
    url = "https://" + region + ".conversation.api.sinch.com/v1/projects/" + Settings.sinch_project_id + "/conversations"

    query = {
    "only_active": "true",
    "app_id": app_id
    }

    response = requests.get(url, params=query, auth=(Settings.sinch_key,Settings.sinch_secret))
    if response.status_code == 200:
        conversationd_list = response.json()
        return conversationd_list
    else:
        return "Something is wrong"

def delete_conversation(conversation_id):
    region = "us"
    url = "https://" + region + ".conversation.api.sinch.com/v1/projects/" + Settings.sinch_project_id + "/conversations/" + conversation_id

    response = requests.delete(url, auth=(Settings.sinch_key,Settings.sinch_secret))
    if response.status_code == 200:
        return "Success"
    else:
        return "Something is wrong"


def configure_webhook(app_id):
    region = "us"
    url = "https://" + region + ".conversation.api.sinch.com/v1/projects/" + Settings.sinch_project_id + "/webhooks"

    payload = {
    "app_id": app_id,
    "target": Settings.base_url + "/webhook/" + app_id,
    "triggers": [
        "MESSAGE_DELIVERY",
        "MESSAGE_INBOUND"
    ]
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers, auth=(Settings.sinch_key,Settings.sinch_secret))
    if response.status_code = 200:
        return response.json()
    else:
        return "Something is wrong"

def delete_webhook(webhook_id):
    region = "us"
    url = "https://" + region + ".conversation.api.sinch.com/v1/projects/" + Settings.sinch_project_id + "/webhooks/" + webhook_id

    response = requests.delete(url, auth=(Settings.sinch_key,Settings.sinch_secret))
    if response.status_code = 200:
        return "Success"
    else:
        return "Something is wrong"