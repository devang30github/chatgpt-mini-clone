from pydantic import BaseModel, EmailStr, Field

class RegisterDTO(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class LoginDTO(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    access_token: str
    user_id: str
