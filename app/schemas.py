from pydantic import BaseModel, EmailStr, Field, validator, json
from pydantic.types import conint
from bson.objectid import ObjectId 
from datetime import datetime
from typing import Optional, Dict


class TextMessage(BaseModel):
    text: str

class ChannelIdentity(BaseModel):
    channel: str
    identity: str
    app_id: str

class ContactMessage(BaseModel):
    text_message: TextMessage

class Message(BaseModel):
    id: str
    direction: str
    contact_message: ContactMessage
    channel_identity: ChannelIdentity
    conversation_id: str
    contact_id: str
    metadata: str
    accept_time: datetime
    sender_id: str
    processing_mode: str
    injected: bool

class MessageMetadata(BaseModel):
    arbitrary: str

class InboundMessageData(BaseModel):
    app_id: str
    accepted_time: datetime
    event_time: datetime
    project_id: str
    message: Message
    message_metadata: MessageMetadata
    correlation_id: str


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if ObjectId.is_valid(v):
            return str(v)
        raise ValueError("Invalid ObjectId")

#need add ProfileName
class ServiceBase(BaseModel):
    service_name : str

class ServiceCreate(BaseModel):
    id : PydanticObjectId = Field(..., alias='_id')
    entity : PydanticObjectId
    services : list[Dict[str,str]]

class PhoneListBase(BaseModel):
    type: str
    phone_number: str

class PhoneListCreate(PhoneListBase):
    pass

class MsgServiceBase(BaseModel):
    msg_service_name : str

class MsgServiceCreate(BaseModel):
    id : PydanticObjectId = Field(..., alias='_id')
    entity : PydanticObjectId
    msgServices : list[Dict[str,str]]
 
class ChatHumanOut(BaseModel):
    human_msg : str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    # entityId: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
