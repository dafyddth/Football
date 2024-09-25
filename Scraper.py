from lxml.html.diff import split_words

import SeleniumChrome
import SeleniumFirefox
from parsel import Selector
def percentage_to_decimal_odds(percentage):
    # Convert the percentage to a decimal
    probability = percentage / 100.0
    # Calculate the decimal odds
    decimal_odds = round(1 / probability,1)
    return decimal_odds

def get_predicted_odds():
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
        home_prob = sel.xpath("//div[@class='fprc']/span[1]/text()").getall()
        draw_prob = sel.xpath("//div[@class='fprc']/span[2]/text()").getall()
        away_prob = sel.xpath("//div[@class='fprc']/span[3]/text()").getall()
        for i in range(10):
            print(home_teams[i],'v', away_teams[i] , percentage_to_decimal_odds(int(home_prob[i+1])),percentage_to_decimal_odds(int(draw_prob[i+1])), percentage_to_decimal_odds(int(away_prob[i+1])))

