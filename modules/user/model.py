from pydantic import BaseModel


class UserListResponse(BaseModel):
    id: int
    name: str


class UserInsertRequest(BaseModel):
    username: str
    password: str


class UserLoginRequest(BaseModel):
    username: str
    password: str


class UserUpdateRequest(BaseModel):
    name: str
