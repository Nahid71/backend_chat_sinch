from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pymongo.mongo_client import MongoClient
from bson import ObjectId
from datetime import datetime
from ..database import get_mongodb
from ..schemas import CreateChatRequest, SMessage
from ..constants import ChannelChoice, SentByChoice
from ..config import settings
from .. import  oauth2

router = APIRouter(
    prefix="/chat",
    tags=['chat']
)

@router.post("/{channel}", status_code=status.HTTP_201_CREATED)
async def create_chat(channel: str, request_data: CreateChatRequest, mongodb: MongoClient = Depends(get_mongodb)):
    # Generate a new chat ID using ObjectId
    chat_id = ObjectId()
    # Define the chat document to be inserted into the database
    print(request_data.domain)

    connector = mongodb.connectors.find_one(
                            {"uri" : request_data.domain}
                        )
    if channel == "shopify" or "whatsapp":
        print("Entites: ", connector["name"])
        chat_collections = mongodb.chats
        if connector == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Domain does not exist")
        chat_doc = {
            "_id": chat_id,
            "channel": ChannelChoice.SHOPIFY_EXTENSION,
            "entity": ObjectId(connector["entity"]),
            "lastMsgTimestamp": datetime.utcnow()
        }
        # store it in database
        new_chat = chat_collections.insert_one(chat_doc)
        if new_chat.inserted_id:
            return {"chat_id": str(chat_id)}
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Chat creation failed")
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Not implemented yet")

@router.get("/{channel}/{chat_id}")
async def chat_messages(channel: str, chat_id: str, mongodb: MongoClient = Depends(get_mongodb)):
    try:
        if channel == "shopify":
            # Convert the provided chat_id to ObjectId
            chat_object_id = ObjectId(chat_id)
            # Retrieve messages from the database for the specified chat_id
            message_collections = mongodb.messages.find({"chat": chat_object_id}).sort("msgTimestamp")
            messages = []
            for message in message_collections:
                messages.append({"chat": str(message["chat"]), 
                                 "sentBy":message["sentBy"], 
                                 "content":message["content"],
                                 "msgTimestamp": message["msgTimestamp"]})
            return {
                "chat_id": chat_id,
                "messages": messages
            }
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Not implemented yet")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{channel}/{chat_id}", status_code=status.HTTP_201_CREATED)
async def create_message(channel: str, chat_id: str, message: SMessage, mongodb: MongoClient = Depends(get_mongodb), current_user: dict = Depends(oauth2.get_current_user)):
    try:
        # Convert the provided chat_id to ObjectId
        chat_object_id = ObjectId(chat_id)
        if channel == "shopify":
            message_doc = {
                "chat": chat_object_id,
                "sentBy": SentByChoice.CONTACT,
                "content": message.text,
                "msgTimestamp": datetime.utcnow()
            }
            new_message = mongodb.messages.insert_one(message_doc)
            # To do
            # call the AI for response
            ai_message = message.text + "from AI"
            # Define the message document
            message_doc = {
                "chat": chat_object_id,
                "sentBy": SentByChoice.AI,
                "content": ai_message,
                "msgTimestamp": datetime.utcnow()
            }
            new_message = mongodb.messages.insert_one(message_doc)
            print("new message: ", new_message)
            if new_message:
                return {
                    "chat": chat_id,
                    "message": ai_message,
                    "status": "Message created successfully"
                }
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Message creation failed")
        else:
            region = "us"
            app_id: current_user.get("app_id")
            url = "https://" + region + ".conversation.api.sinch.com/v1/projects/" + settings.sinch_project_id + "/messages:send"

            payload = {
            "app_id": app_id,
            "recipient": {
                "identified_by": {
                    "channel_identities": [
                        {
                            "channel": "whatsapp",
                            # the contact to which you want to send the message.

                            "identity": " +919999999999" 
                        }  
                        ]
                }
            },
            "message": {
                "text_message": {
                    "text": "Text message from Sinch Conversation API."
                }
            }  
            }   
            headers = {"Content-Type": "application/json",
              "Authorization": "Basic " + settings.secret_key }#take from dashboard
            response = requests.post(url, json=payload, headers=headers, auth=(settings.sinch_key,settings.sinch_secret))
            # if message is sent successfully then store it in database
            if response.status_code == 200:
                message_doc = {
                    "chat": chat_object_id,
                    "sentBy": SentByChoice.CONTACT,
                    "content": message.text,
                    "msgTimestamp": datetime.utcnow()
                }
                new_message = mongodb.messages.insert_one(message_doc)
                if new_message:
                    return {
                        "chat": chat_id,
                        "message": message.text,
                        "status": "Message created successfully"
                    }
                else:
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Message creation failed")
            print(response)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))