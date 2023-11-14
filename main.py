import schedule
import time
from attendance import job


schedule.every().day.at("09:00").excepted_day_of_week([schedule.friday, schedule.saturday]).do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
