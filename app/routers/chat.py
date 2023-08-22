from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel, HttpUrl
from sinch import Client
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db, get_mongodb
from ..sinch import get_sinch_client, webhook_url

router = APIRouter(
    prefix="/chats",
    tags=['chats']
) 

@router.post("/manager", status_code=status.HTTP_201_CREATED)
async def init_chats(
    request: Request,
    mongodb: MongoClient = Depends(get_mongodb),
    sinch_client: Client = Depends(get_sinch_client)  
):
    sinch_payload = await request.form()
    sinch_payload = jsonable_encoder(sinch_payload)
    print(sinch_payload)

    profile_name = sinch_payload['ProfileName']

    test_db = mongodb.test
    preference_collection = test_db.preferences
    entities_collection = test_db.entities

    msg_service = preference_collection.find_one(
        {'msgServices.sinch_msg_service_id': sinch_payload['MessagingServiceSid']}
    )

    print(msg_service)

    entity = entities_collection.find_one({"_id": msg_service['entity']})
    company_name = entity["name"]

    # assuming only one service per user TO BE fixed
    business_service = msg_service["services"][0]

    print(business_service['sinch_service_id'])

    # Rest of your logic here


    # Example Sinch API call to send a message
    sinch_response = await sinch_client.conversation.messaging.send_message(
        conversation_id, msg_body, webhook_url
    )

    return {"message": "ok"}
