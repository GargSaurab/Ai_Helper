from pydantic import BaseModel
from app.dependencies import SessionDep
from app.models.request.user_registeration_request import UserRegistrationRequest

class UserService(BaseModel):
    
    def __init__(self, db_session : SessionDep ):
       self.db = db_session
       
    def register(self, user_registeration_request : UserRegistrationRequest):
        pass    
   
        