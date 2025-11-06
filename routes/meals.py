from fastapi import APIRouter,HTTPException
from models.Model import updateConsumptionStatus,Meals,UpdateMeals, MealStatus
from bson.objectid import ObjectId
from config.db import Database
from utils.reminder import schedule_meal_reminder,schedule_daily_status,reschedule_meal_reminder
from zoneinfo import ZoneInfo
from config.db import MEAL_COLLECTION,SERVER_TIMEZONE
meals_router=APIRouter(prefix="/meals",tags=["Meals"])
##gets user meal plan
@meals_router.get("/{user_id}")
def get_meal_plan(user_id:str):
     meals_collection=Database.get_collection(MEAL_COLLECTION)

     meal_plans=meals_collection.find({"user_id":user_id},{"time_slot_type":1,"time_slot":1,"foods":1,"status":1})
     print(meal_plans)
     datas=list(meal_plans)
     for data in datas:
          data["_id"]=str(data["_id"])
     return {
          "message":"DATA successfully extracted",
          "data":datas
     }

     

#create meals
@meals_router.post("/create",status_code=201)
def create_meal_plan(meals:Meals):
        meals_collection=Database.get_collection(MEAL_COLLECTION)
        
        is_exist=meals_collection.find_one(
            {"user_id":meals.user_id,
             "time_slot_type":meals.time_slot_type})
        print(is_exist)
        if  is_exist :
            raise HTTPException(status_code=400,detail="we cannot create same time slot plan")
        try:
            schedule_meal_reminder(user_id=meals.user_id,time=meals.time_slot,slot_name=meals.time_slot_type.value)
            schedule_daily_status(user_id=meals.user_id,time=meals.time_slot)
            
        except:
            raise HTTPException(
                status_code=400,
                detail="try again later"
            )
        meals.time_slot=meals.time_slot.astimezone(ZoneInfo(SERVER_TIMEZONE))
        print("SSSS",meals.time_slot)
        meals.job_id=f"{meals.user_id}_{meals.time_slot_type}"
        data=meals_collection.insert_one(dict(meals))
        print(data)
        return {"message":"Meal plan created successfully","data":str(data.inserted_id)}
            

#update meals
@meals_router.patch("/update/{meal_id}",status_code=200)
def update_meal_plan(meal_id:str,meal:UpdateMeals):
    collection=Database.get_collection(MEAL_COLLECTION)
    object_id=ObjectId(meal_id)
    meals=collection.find_one({"_id":object_id})
    print(meals)
    if not meals :
        raise HTTPException(
            status_code=404,
            detail=" user not found please register first"
     )
    try:
            reschedule_meal_reminder(
                 job_id=meals["job_id"],
                 time=meal.time_slot)
    except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"try again later {e}"
            )
    
    updated_data = collection.update_one({"_id":object_id},{"$set":{"foods":meal.foods,"time_slot":meal.time_slot}})
    return {"message":" meal plan updated successfully"}
      


@meals_router.patch("/consume/{meal_id}")
def consumption_status(meal_id:str,body:updateConsumptionStatus):
    meal_id_obj=ObjectId(meal_id)
    meals_col=Database.get_collection(MEAL_COLLECTION)
    is_exist=meals_col.find_one({"_id":meal_id_obj})
    if not is_exist:
     raise HTTPException(
        status_code=400,
        detail="meal plan not found")
    if body.status!=MealStatus.completed:
         raise HTTPException(
        status_code=400,
        detail="credentials is wrong")
    meals_col.update_one({"_id":meal_id_obj},{"$set":{"status":body.status}})
    return {"message":f"{MealStatus.completed} meal   compeleted successfully"}
       
