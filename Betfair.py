import betfairlightweight
from selenium.webdriver.common.devtools.v85.database import Database

import Database as DBS
from betfairlightweight import filters
from datetime import datetime

un = 'dafyddth'
pw = 'HydrefY4ydd'
key = 'n5AokgBdioLBhTNk'
cert = 'C:\\Certs'
now = datetime.now()
formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")


def get_home_team(match):
    # Split the string by ' V ' and return the first part
    home_team = match.split(' v ')[0]
    return home_team


def get_away_team(match):
    # Split the string by ' V ' and return the second part
    away_team = match.split(' v ')[1]
    return away_team

def get_betfair_data(current_date_time, session_id):
    # Create a trading instance
    trading = betfairlightweight.APIClient(un, pw, key, certs=cert)

    # Login
    trading.login()

    # Create a market filter for soccer competitions
    soccer_filter = filters.market_filter(competition_ids=['10932509'])

    # List events
    events = trading.betting.list_events(soccer_filter)
    for e in events:
        # print(e.event.name, e.event.open_date.date(), e.event.id)
        # Create a market filter for match odds market
        market_filter = filters.market_filter(event_ids=[e.event.id], market_type_codes=['MATCH_ODDS'])

        # List market catalogues
        market_catalogues = trading.betting.list_market_catalogue(
            filter=market_filter,
            max_results='1',  # Limit to 1 result for simplicity
            market_projection=['RUNNER_METADATA']
        )

        for market in market_catalogues:
            # List market books to get the latest odds
            market_books = trading.betting.list_market_book(
                market_ids=[market.market_id],
                price_projection=filters.price_projection(price_data=['EX_BEST_OFFERS'])
            )
            event_list = (
                e.event.id, market.market_id, e.event.open_date.date().isoformat(), e.event.open_date.time().isoformat(),
                e.event.name,
                get_home_team(e.event.name), get_away_team(e.event.name))
            # print(event_list)
            DBS.insert_match_details(event_list[0], event_list[1], event_list[2], event_list[3], event_list[4], event_list[5], event_list[6], session_id)

            for market_book in market_books:
                home_back_odds = 0
                home_lay_odds = 0
                away_back_odds = 0
                away_lay_odds = 0
                draw_back_odds = 0
                draw_lay_odds = 0
                for runner in market_book.runners:
                    if runner.selection_id == market.runners[0].selection_id:
                        home_back_odds = runner.ex.available_to_back[0].price if runner.ex.available_to_back else None
                        home_lay_odds = runner.ex.available_to_lay[0].price if runner.ex.available_to_lay else None
                    elif runner.selection_id == market.runners[1].selection_id:
                        away_back_odds = runner.ex.available_to_back[0].price if runner.ex.available_to_back else None
                        away_lay_odds = runner.ex.available_to_lay[0].price if runner.ex.available_to_lay else None
                    elif runner.selection_id == market.runners[2].selection_id:
                        draw_back_odds = runner.ex.available_to_back[0].price if runner.ex.available_to_back else None
                        draw_lay_odds = runner.ex.available_to_lay[0].price if runner.ex.available_to_lay else None


                DBS.insert_betfair_odds(e.event.id, market.market_id, formatted_now, home_back_odds, home_lay_odds, away_back_odds,
                                        away_lay_odds, draw_back_odds, draw_lay_odds, session_id)


    # Logout
    DBS.correct_team_names()
    trading.logout()
