import Betfair
import Scraper
import datetime
import Database as db


now = datetime.datetime.now()
current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
session_id = int(now.strftime("%Y%m%d%H%M%S"))
Betfair.get_betfair_data(current_date_time, session_id)
Scraper.get_predicted_odds(current_date_time, session_id,'forebet')
Scraper.get_predicted_odds(current_date_time, session_id,'predictz')
db.update_marketids()
print(session_id)
print(current_date_time)
print("Main Finished")
