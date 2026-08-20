from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr


class LoginRequest(BaseModel):
    """Body for the login endpoint."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Successful authentication response."""

    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str = "bearer"
