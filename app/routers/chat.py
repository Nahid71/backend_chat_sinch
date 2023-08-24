from fastapi import APIRouter, status, Depends, Request
from fastapi.encoders import jsonable_encoder
from ..database import get_mongodb

router = APIRouter(
    prefix="/chats",
    tags=['chats']
) 

# @router.post("/manager", status_code=status.HTTP_201_CREATED)
# async def init_chats(
#     request: Request,
#     mongodb: MongoClient = Depends(get_mongodb),
#     sinch_client: Client = Depends(get_sinch_client)  
# ):
#     sinch_payload = await request.form()
#     sinch_payload = jsonable_encoder(sinch_payload)
#     print(sinch_payload)

#     profile_name = sinch_payload['ProfileName']

#     test_db = mongodb.test
#     preference_collection = test_db.preferences
#     entities_collection = test_db.entities

#     msg_service = preference_collection.find_one(
#         {'msgServices.sinch_msg_service_id': sinch_payload['MessagingServiceSid']}
#     )

#     print(msg_service)

#     entity = entities_collection.find_one({"_id": msg_service['entity']})
#     company_name = entity["name"]

#     # assuming only one service per user TO BE fixed
#     business_service = msg_service["services"][0]

#     print(business_service['sinch_service_id'])

#     # Rest of your logic here


#     # Example Sinch API call to send a message
#     sinch_response = await sinch_client.conversation.messaging.send_message(
#         conversation_id, msg_body, webhook_url
#     )

#     return {"message": "ok"}


# api for sead a message
# method for a create a conversation 
# api get a conversation and it's messages
# delete a conversation


# weebhook