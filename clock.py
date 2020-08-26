from apscheduler.schedulers.blocking import BlockingScheduler
from seed_demo import seed_demo

seedSched = BlockingScheduler()

@seedSched.scheduled_job('interval', minutes=5)
def cleanupDatabase():
    print("Cleaning up database and reseeding with demo account data.")
    seed_demo()

seedSched.start()