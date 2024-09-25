import Betfair
import Scraper
import datetime

now = datetime.datetime.now()
current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
session_id = int(now.strftime("%Y%m%d%H%M%S"))
Betfair.get_betfair_data(current_date_time, session_id)
Scraper.get_predicted_odds()
print(session_id)
