from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
import requests
from ..config import Settings
from .. import schemas, oauth2
from ..database import get_mongodb
from pymongo.mongo_client import MongoClient


router = APIRouter(
    prefix="/services",
    tags=['services']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ServiceCreate)
def create_service(
    service: schemas.ServiceBase,
    mongodb: MongoClient = Depends(get_mongodb),
    current_user: dict = Depends(oauth2.get_current_user)
):
    test_db = mongodb.test
    preference_collection = test_db.preferences
    region = "us"
    
    url = "https://" + region + ".conversation.api.sinch.com/v1/projects/" + Settings.sinch_project_id + "/apps"
    payload = {
    "channel_credentials": [
        {
        "channel": "WHATSAPP",
        "static_token": {
            "token": "{Facebook_Token}"
        }
        }
    ],
    "display_name": "Demo Facebook App"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers, auth=(Settings.sinch_key,Settings.sinch_secret))
    app_data = response.json()
    updated_pref = preference_collection.find_one_and_update(
        {"entity": current_user["entity"]},
        {"$addToSet": {"services": app_data}},
        return_document=True,
    )

    return updated_pref

## TO DO

# Create three more route for get, list and delete app