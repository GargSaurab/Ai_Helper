from app.models.request.user_registration_request import UserRegistrationRequest
from app.db.repositories.user_repository import UserRepository

class UserService:
    
    def __init__(self, userRepo: UserRepository):
        self.userRepo = userRepo
       
    def register(self, user_registeration_request: UserRegistrationRequest):
        pass    
   
        