
from datetime import datetime
from config.job import Job
from zoneinfo import ZoneInfo
from config.db import Database,MEAL_COLLECTION,SERVER_TIMEZONE
# connect jobstore to your MongoDB



def meal_notify(user_id:str,slot_name:str):
    '''
    Here push notification will trigger with 3rd party notfication services
    '''
    print("REMINDER please take Meal")
    

def schedule_meal_reminder(user_id:str,slot_name:str,time:datetime):
    local_tme=time.astimezone(ZoneInfo(SERVER_TIMEZONE))
    Job.create_job(

        func=meal_notify,
        func_args=[user_id,slot_name],
        job_time=local_tme,
        job_id=f"{user_id}_{slot_name}"  
        )

def reschedule_meal_reminder(job_id:str,time:datetime):
    local_tme=time.astimezone(ZoneInfo(SERVER_TIMEZONE))
    Job.update_job(
        job_id=job_id,
        updated_time=local_tme)



def change_meal_status(user_id:str):
    '''
    changing meal status of meal plan
    '''
    collection=Database.get_collection(MEAL_COLLECTION)
    collection.update_many({"user_id":user_id},{
        "$set":{
            "status":"pending",
        }
    })

def schedule_daily_status(user_id:str,time:datetime):
    '''
    every midnight  with resepctive time zone of user status will change this is a schedule job
    '''
    midnight_time=time.replace(hour=00,minute=00,second=00)
    print(midnight_time)
    local_tme=midnight_time.astimezone(ZoneInfo(SERVER_TIMEZONE))
    Job.create_job(
         func=change_meal_status,
        func_args=[user_id],
        job_time=local_tme,
        job_id=f"{user_id}_status"  
        )
    