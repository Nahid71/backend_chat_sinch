from pydantic import BaseModel, EmailStr, Field, validator, json
from pydantic.types import conint
from bson.objectid import ObjectId 
from datetime import datetime
from typing import Optional, Dict



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
