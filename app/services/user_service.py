from pydantic import BaseModel

class UserService(BaseModel):
    
    __init__(self, db_session : DbSession):
        