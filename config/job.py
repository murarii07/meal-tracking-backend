
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from datetime import datetime
from apscheduler.triggers.cron import CronTrigger
from zoneinfo import ZoneInfo
from config.db import JOB_COLLECTION,DB_NAME,SERVER_TIMEZONE


class Job:
    scheduler=None
    
    @classmethod
    def start_jobs(cls):
        try:
            job_stores = {'default': MongoDBJobStore(database=DB_NAME, collection=JOB_COLLECTION)}
            config = {
            "apscheduler.timezone": "Asia/Kolkata",
            "apscheduler.jobstores.default": {
            "type": "mongodb",
            "database": DB_NAME,
            "collection": JOB_COLLECTION
            }}
         
            cls.scheduler = BackgroundScheduler(config)
            cls.scheduler.start()
            print("Jobs scheduling started!!")
        except Exception as e:
            print("something went wrong")

    @classmethod
    def create_job(cls,func,job_id:str,job_time:datetime,func_args:list):
      
            cls.scheduler.add_job(
            func=func,
            trigger=CronTrigger(hour=job_time.hour, minute=job_time.minute,timezone=ZoneInfo(SERVER_TIMEZONE)),
            id=job_id,
            args=func_args,
            replace_existing=True,
            misfire_grace_time=100
        )
            print("JOB create scuessfully")

    @classmethod
    def update_job(cls,job_id:str,updated_time:datetime):
         trigger=CronTrigger(hour=updated_time.hour, minute=updated_time.minute,timezone=ZoneInfo(SERVER_TIMEZONE))
         cls.scheduler.reschedule_job(job_id=job_id,trigger=trigger)
         print("Job updated successfully")


     

    

        

