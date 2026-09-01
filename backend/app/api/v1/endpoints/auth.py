from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.core.client_ip import get_client_ip
from app.schemas.auth import TokenResponse
from app.services import auth_service

router = APIRouter()


@router.post("/token", response_model=TokenResponse)
async def login(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenResponse:
    """Authenticate with admin credentials and receive a bearer token."""
    token = auth_service.authenticate(form_data.username, form_data.password, client_ip=get_client_ip(request))
    return TokenResponse(access_token=token)
