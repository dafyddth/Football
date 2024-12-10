from betfairlightweight.compat import parse_datetime
from lxml.html.diff import split_words
import Database as DBS
import SeleniumChrome
import SeleniumFirefox
from datetime import datetime
import functions as f

from parsel import Selector
from selenium.webdriver.common.devtools.v85.database import Database

#current_datetime = datetime.strptime(current_date_time, '%Y-%m-%d %H:%M:%S')


def datetime_from_string(date_time_string):
    date_formats = ['%d/%m/%Y %H:%M', '%d/%m/%Y']
    for date_format in date_formats:
        try: 
            datetime_obj = datetime.strptime(date_time_string, date_format)
            return datetime_obj
        except ValueError:
            continue
    raise ValueError("Date string does not match any expected format")



def get_predicted_odds(current_date_time, session_id, site):
    forebet_url = "https://www.forebet.com/en/football-tips-and-predictions-for-england/premier-league"
    predictz_url = "https://www.predictz.com/predictions/england/premier-league/"

    if site == 'forebet':
        website = forebet_url
    elif site == 'predictz':
        website = predictz_url
    else:
        raise ValueError("Unsupported site")
    html = SeleniumFirefox.get_page_source(website)

    sel = Selector(html)
    if website == predictz_url:
        print(sel.xpath("//tr[@class='pzcnth']/td/h2/text()").getall())

        print(sel.xpath("//td[@class='fixt']/a/text()").getall())
        matches = sel.xpath("//td[@class='fixt']/a/text()").getall()
        odds = sel.xpath("//td[@class='odds']/a/text()").getall()
        match_counter = 0
        for match in matches:
            print(match)
            teams = match.split('vs')
            home_team = teams[0]
            away_team = teams[1]
            home_odds = odds[match_counter]
            draw_odds = odds[match_counter + 1]
            away_odds = odds[match_counter + 2]
            match_counter += 3

            print(home_team, away_team, home_odds, draw_odds, away_odds)
            DBS.insert_predictz_odds(current_date_time, home_odds, draw_odds, away_odds, home_team, away_team, session_id)
            DBS.correct_team_names()
            DBS.update_predictz_table()
        print("no of matches ", len(matches))
        print("no of odds ", len(odds))




    elif website == forebet_url:
        home_teams = sel.xpath("//span[@class='homeTeam']/span[@itemprop='name']/text()").getall()
        away_teams = sel.xpath("//span[@class='awayTeam']/span[@itemprop='name']/text()").getall()
        match_date_time = sel.xpath("//time[@itemprop='startDate']/span[@class='date_bah']/text()").getall()
        home_prob = sel.xpath("//div[@class='fprc']/span[1]/text()").getall()
        draw_prob = sel.xpath("//div[@class='fprc']/span[2]/text()").getall()
        away_prob = sel.xpath("//div[@class='fprc']/span[3]/text()").getall()
        print("no_home_prob", len(home_prob))
        for i in range(len(home_prob) - 1):  # REPLACE WITH HOME TEAMS COUNT
            print(i)
            print(home_teams[i])
            home_odds = f.percentage_to_decimal_odds(int(home_prob[i + 1]))
            draw_odds = f.percentage_to_decimal_odds(int(draw_prob[i + 1]))
            away_odds = f.percentage_to_decimal_odds(int(away_prob[i + 1]))
            match_date = f.date_from_string(match_date_time[i])
            match_time = f.time_from_string(match_date_time[i]).strftime('%H:%M:%S')
            print(match_date_time[i], current_date_time, home_teams[i], 'v', away_teams[i], home_prob[i + 1], home_odds,
                  draw_odds, away_odds)
            print(match_date)
            print(match_time)
            
            match_datetime = datetime_from_string(match_date_time[i])
            if match_datetime > datetime.strptime(current_date_time, '%Y-%m-%d %H:%M:%S'):
                DBS.insert_forebet_odds(current_date_time, home_odds, draw_odds, away_odds, session_id, home_teams[i],
                                        away_teams[i], match_date, match_time)
                DBS.correct_team_names()
