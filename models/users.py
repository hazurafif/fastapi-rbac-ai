from pydantic import BaseModel

class LoginModel(BaseModel):
    email: str
    password: str
    
class UsersTable:
    def insert_new_user(self):
        return

Users = UsersTable()