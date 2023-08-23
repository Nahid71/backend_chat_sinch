from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from ..schemas import InboundMessageData
router = APIRouter(
    prefix="/webhook",
    tags=['webhook']
)


@router.post("/{app_id}", status_code=status.HTTP_201_CREATED)
def create_service(inbound_msg:InboundMessageData):
    # process received message
    return 