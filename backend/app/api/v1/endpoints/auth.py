from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import TokenResponse
from app.services import auth_service

router = APIRouter()


@router.post("/token", response_model=TokenResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenResponse:
    """Authenticate with admin credentials and receive a bearer token."""
    token = auth_service.authenticate(form_data.username, form_data.password)
    return TokenResponse(access_token=token)
