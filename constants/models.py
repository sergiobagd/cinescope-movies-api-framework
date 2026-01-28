from pydantic import BaseModel, Field, field_validator
from typing import Optional
from constants.roles import Roles
import datetime

class TestUser(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str = Field(..., min_length=1, max_length=20, description="Passwords should be equal")
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("email")
    def check_email(cls, value: str) -> str:
        if not "@" in value:
            raise ValueError(f"There is no @ in email")
        return value

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        # Check passwords match
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Passwords don't match")
        return value

    # Custom JSON serializator for Enum
    class Config:
        json_encoders = {
            Roles: lambda v: v.value # Enum -> string
        }



class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    verified: bool
    banned: bool
    roles: list[Roles]
    createdAt: str

    @field_validator("createdAt")
    def check_created_at(cls, value: str) -> str:
        # Validate format of date and time (ISO 8601).
        try:
            datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("Incorrect format of date and time")
        return value

class AuthenticateUser(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    roles: list[Roles]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

class AuthenticatedUserResponse(BaseModel):
    user: AuthenticateUser
    accessToken: str
    expiresIn: int