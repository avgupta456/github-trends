from pydantic import BaseModel

"""
Input Models
"""


class CreateUserModel(BaseModel):
    user_id: str
    access_token: str


"""
Database Models
"""


class UserModel(BaseModel):
    user_id: str
    access_token: str
