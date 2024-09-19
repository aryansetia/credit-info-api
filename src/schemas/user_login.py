from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
        json_schema_extra = {
            "examples": [
                {
                    "username": "john_doe",
                    "password": "1234"
                }
            ]
        }