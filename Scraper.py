from lxml.html.diff import split_words
import Database as DBS
import SeleniumChrome
import SeleniumFirefox
from datetime import datetime
import functions as f

from parsel import Selector
from selenium.webdriver.common.devtools.v85.database import Database



def get_predicted_odds(current_date_time, session_id):
    bbc = "https://www.bbc.co.uk"
    forebet = "https://www.forebet.com/en/football-tips-and-predictions-for-england/premier-league"
    betfair = "https://www.betfair.com/exchange/plus/en/football/english-premier-league-betting-10932509"
    predictz = "https://www.predictz.com/predictions/england/premier-league/"
    website = forebet
    html = SeleniumFirefox.get_page_source(website)

    sel = Selector(html)
    if website == predictz:
        print(sel.xpath("//td[@class='fixt']/a/text()").getall())
        matches = sel.xpath("//td[@class='fixt']/a/text()").getall()
        for match in matches:
            print(match)


    elif website == forebet:
        home_teams = sel.xpath("//span[@class='homeTeam']/span[@itemprop='name']/text()").getall()
        away_teams = sel.xpath("//span[@class='awayTeam']/span[@itemprop='name']/text()").getall()
        match_date_time = sel.xpath("//time[@itemprop='startDate']/span[@class='date_bah']/text()").getall()
        home_prob = sel.xpath("//div[@class='fprc']/span[1]/text()").getall()
        draw_prob = sel.xpath("//div[@class='fprc']/span[2]/text()").getall()
        away_prob = sel.xpath("//div[@class='fprc']/span[3]/text()").getall()

        for i in range(15): # REPLACE WITH HOME TEAMS COUNT
            home_odds = f.percentage_to_decimal_odds(int(home_prob[i + 1]))
            draw_odds = f.percentage_to_decimal_odds(int(draw_prob[i + 1]))
            away_odds = f.percentage_to_decimal_odds(int(away_prob[i + 1]))
            match_date = f.date_from_string(match_date_time[i])
            match_time = f.time_from_string(match_date_time[i]).strftime('%H:%M:%S')
            print(match_date_time[i] , current_date_time, home_teams[i],'v', away_teams[i] , home_odds, draw_odds, away_odds)
            print(match_date)
            print(match_time)

            match_datetime = datetime.strptime(match_date_time[i], '%d/%m/%Y %H:%M')
            current_datetime = datetime.strptime(current_date_time, '%Y-%m-%d %H:%M:%S')
            if match_datetime > current_datetime:
                DBS.insert_forebet_odds(current_date_time, home_odds, draw_odds, away_odds, session_id, home_teams[i], away_teams[i], match_date, match_time )
