from dotenv import load_dotenv
import time
import schedule
from sheets import run

'''
Schedule Documentation: https://schedule.readthedocs.io/en/stable/
'''

# periodically retrieve the phone numbers and weeks postpartum from gSheets
def dailyUpdate():
    print('Updating...')
    run()

if __name__ == '__main__':
   
    load_dotenv('/.env') 
    
    print('Running script...')
    schedule.every().minutes.do(dailyUpdate)
    
    while True:
        schedule.run_pending()
        time.sleep(1)