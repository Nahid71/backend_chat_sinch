from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from ..sinch import get_sinch_client
from .. import schemas, oauth2
from ..database import get_mongodb
import requests
from ..config import Settings
from pymongo.mongo_client import MongoClient


router = APIRouter(
    prefix="/phonelist",
    tags=['phonelist']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PhoneListCreate)
async def add_phone(
    mongodb: MongoClient = Depends(get_mongodb),
    current_user: dict = Depends(oauth2.get_current_user)
    ):
    url = "https://numbers.api.sinch.com/v1/projects/" + Settings.sinch_project_id + "/availableNumbers"

    payload = {
    "regionCode": "US",
    "type": "LOCAL",
    "capabilities": [
        "SMS"
    ],
    "numberPattern": {
        "pattern": "+1208",
        "searchPattern": "START"
    },
    "smsConfiguration": {
        "servicePlanId": "YOUR_SMS_servicePlanId", # store in .env file
        "campaignId": "YOUR_campaignId_from_TCR" # store in .env file
    }
    }
    # TO do
    # only store necessary data into database
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers, auth=(Settings.sinch_key,Settings.sinch_secret))

    data = response.json()
    ## To Do
    ## enable for whatsapp message


    test_db = mongodb.test
    preference_collection = test_db.preferences
    updated_pref = preference_collection.find_one_and_update(
                            {"entity" : current_user["entity"]}, 
                            {"$addToSet": { "phoneBindings":  data }  },
                            return_document=True,
                        )
    # todo
    # Create a schema for phone objects
    return updated_pref
    

@router.get("/", response_model=schemas.PhoneListCreate)
def list_services(mongodb : MongoClient = Depends(get_mongodb),
                current_user: dict = Depends(oauth2.get_current_user)):

    test_db = mongodb.test
    preference_collection = test_db.preferences

    entity_phones = preference_collection.find_one(
                            {"entity" : current_user["entity"]}
                        )
    # todo
    # Create a schema for phone objects
    return entity_phones

@router.delete("/{phone_num}", status_code=status.HTTP_204_NO_CONTENT)
def del_phone( phone_num : str, phone_type : str,
                    mongodb : MongoClient = Depends(get_mongodb),
                    current_user: dict = Depends(oauth2.get_current_user)):

    test_db = mongodb.test
    preference_collection = test_db.preferences

    entity_phones = preference_collection.find_one(
                            {"entity" : current_user["entity"]}
                        )

    if entity_phones == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"phone number does not exist")

    
    tmp_dict = {"type":phone_type, "phone_number" : phone_num}


    updated_pref = preference_collection.find_one_and_update(
                            {"entity" : current_user["entity"]}, 
                            {"$pull": { "phoneBindings":  tmp_dict }  }
                        )

    return {"message" : "deleted"}