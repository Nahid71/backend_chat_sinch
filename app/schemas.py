from pydantic import BaseModel, EmailStr, Field
from bson.objectid import ObjectId 
from datetime import datetime
from typing import  Dict, List


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


class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: ObjectId) -> str:
        if not isinstance(v, ObjectId):
            raise TypeError('ObjectId required')
        return str(v)

#need add ProfileName
class ServiceBase(BaseModel):
    service_name : str

class ServiceItem(BaseModel):
    key: str
    value: str

class ServiceCreate(BaseModel):
    id : PydanticObjectId = Field(..., alias='_id')
    entity : PydanticObjectId
    services : List[ServiceItem]

class PhoneListBase(BaseModel):
    type: str
    phone_number: str

class PhoneListCreate(PhoneListBase):
    pass

class MsgServiceBase(BaseModel):
    msg_service_name : str
 
class ChatHumanOut(BaseModel):
    human_msg : str

