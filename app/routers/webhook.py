from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from ..schemas import InboundMessageData
router = APIRouter(
    prefix="/webhook",
    tags=['webhook']
)


@router.post("/inbound_message/{app_id}", status_code=status.HTTP_201_CREATED)
def inbound_message(inbound_msg:InboundMessageData):
    # process received message
    return 

@router.post("/message_delivery/{app_id}", status_code=status.HTTP_201_CREATED)
def message_delivery(inbound_msg:InboundMessageData):
    # process message delivery event
    return 