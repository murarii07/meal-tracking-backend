from pydantic import BaseModel,Field
from datetime import time,datetime
from typing  import Optional
from enum import Enum



class TimeSlot(str,Enum):
    morning="morning"
    afternoon="afternoon"
    evening="evening"
    night="night"


class MealStatus(str,Enum):
    completed="completed"
    pending="pending"


class UserCreation(BaseModel):
    username:str
    password:str

class User(BaseModel):
    username:str
    password:str


class Meals(BaseModel):
    user_id:str #userID of User
    status:Optional[MealStatus]=MealStatus.pending
    time_slot:datetime
    time_slot_type:TimeSlot
    foods:list=Field(...,min_length=1)
    job_id:Optional[str]=None #job_id

class UpdateMeals(BaseModel):
    foods:list
    time_slot:Optional[datetime]=None


class updateConsumptionStatus(BaseModel):
    status:MealStatus=MealStatus.pending