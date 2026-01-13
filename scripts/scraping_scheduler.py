import schedule
import time
from scrape_and_save import scrape_and_save_data, scrape_and_save_data2, scrape_and_save_data3

def scheduled_task():
    print("Scheduled task running...")
    scrape_and_save_data()
    scrape_and_save_data2()
    scrape_and_save_data3()
    

schedule.every().day.at("00:00").do(scheduled_task)

while True:
    schedule.run_pending()
    time.sleep(60)
