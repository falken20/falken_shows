from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.client_ip import get_client_ip
from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.auth import TokenResponse
from app.services import auth_service

router = APIRouter()


@router.post("/token", response_model=TokenResponse)
async def login(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenResponse:
    """Authenticate with admin credentials and receive a bearer token."""
    token = await auth_service.authenticate(
        form_data.username,
        form_data.password,
        session=db,
        client_ip=get_client_ip(request),
    )
    return TokenResponse(access_token=token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def logout(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[dict[str, Any], Depends(get_current_user)],
) -> None:
    """Revoke the current access token."""
    await auth_service.revoke_access_token(db, user)
