import sqlite3


# Insert Match Details
def insert_match_details(bf_event_id, bf_market_id, match_date, match_time, match, home_team, away_team, session_id):
    sql = (f"INSERT OR IGNORE INTO Market (BFEventID, BFMarketID, Date, Time, Match, HomeTeam, AwayTeam, SessionID) "
           f"VALUES ("
           f" {bf_event_id}, {bf_market_id}, '{match_date}', '{match_time}', '{match}', '{home_team}', '{away_team}','{session_id}');")
    # Connect to a database (or create one if it doesn't exist)
    # print(sql)
    conn = sqlite3.connect('Football.db')
    # Create a cursor object to interact with the database
    cursor = conn.cursor()
    cursor.execute(sql)
    # Save (commit) the changes
    conn.commit()
    conn.close()


def insert_betfair_odds(bf_event_id, bf_market_id, odds_date, bf_home_back_odds, bf_home_lay_odds, bf_away_back_odds,
                        bf_draw_back_odds,
                        bf_away_lay_odds, bf_draw_lay_odds, session_id):
    sql = ("INSERT INTO BetfairOdds (BFEventID, BFMarketID, OddsDate, BFHomeBackOdds, BFHomeLayOdds, BFAwayBackOdds, "
           " BFAwayLayOdds, BFDrawBackOdds,  BFDrawLayOdds, SessionID) "
           "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);")
    conn = sqlite3.connect('Football.db')
    cursor = conn.cursor()
    cursor.execute(sql, (bf_event_id, bf_market_id, odds_date, bf_home_back_odds, bf_home_lay_odds, bf_away_back_odds,
                         bf_draw_back_odds, bf_away_lay_odds, bf_draw_lay_odds, session_id))
    conn.commit()
    conn.close()


def insert_forebet_odds(odds_date, home_odds, draw_odds, away_odds, session_id, home_team, away_team, match_date,
                        match_time):
    sql = "INSERT INTO Forebetodds(OddsDate, FBHomeBackOdds, FBDrawBackOdds, FBAwayBackOdds, SessionID, HomeTeam, AwayTeam, MatchDate, MatchTime)" \
          " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    conn = sqlite3.connect('Football.db')
    cursor = conn.cursor()
    cursor.execute(sql, (
        odds_date, home_odds, draw_odds, away_odds, session_id, home_team, away_team, match_date, match_time))
    conn.commit()
    conn.close()


def insert_predictz_odds(odds_date, home_odds, draw_odds, away_odds, home_team, away_team, session_id):
    sql = "INSERT INTO PredictzOdds (OddsDate, PZHomeBackOdds, PZAwayBackOdds, PZDrawBackOdds, HomeTeam, AwayTeam, SessionID)" \
          " VALUES(?,?,?,?,?,?,?)"
    conn = sqlite3.connect('Football.db')
    cursor = conn.cursor()
    cursor.execute(sql, (odds_date, home_odds, draw_odds, away_odds, home_team, away_team, session_id))
    conn.commit()
    conn.close()


def update_predictz_table():
    sql = """
WITH UpdateSource AS (
    SELECT DISTINCT B.SessionID,
                    M.Date,
                    M.Time,
                    M.HomeTeam
      FROM BetfairOdds B
           INNER JOIN
           Market M ON B.BFMarketID = M.BFMarketID
)
UPDATE PredictzOdds
   SET MatchDate = (
           SELECT U.Date
             FROM UpdateSource U
            WHERE PredictzOdds.SessionID = U.SessionID AND 
                  PredictzOdds.HomeTeam = U.HomeTeam
       ),
       MatchTime = (
           SELECT U.Time
             FROM UpdateSource U
            WHERE PredictzOdds.SessionID = U.SessionID AND 
                  PredictzOdds.HomeTeam = U.HomeTeam
       );

    """
    conn = sqlite3.connect('Football.db')
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


def correct_team_names():
    conn = sqlite3.connect('Football.db')
    cursor = conn.cursor()
    sql = "update Market SET HomeTeam = trim(HomeTeam), AwayTeam = trim(AwayTeam);"
    cursor.execute(sql)
    sql = ("UPDATE Market SET HomeTeam = tblTeamDictionary.CorrectName FROM "
           "tblTeamDictionary WHERE Market.HomeTeam = tblTeamDictionary.originalName")
    cursor.execute(sql)
    sql = ("UPDATE Market SET AwayTeam = tblTeamDictionary.CorrectName FROM "
           "tblTeamDictionary WHERE Market.AwayTeam = tblTeamDictionary.originalName")
    cursor.execute(sql)
    sql = ("UPDATE ForebetOdds SET HomeTeam = tblTeamDictionary.CorrectName FROM "
           "tblTeamDictionary WHERE trim(ForebetOdds.HomeTeam) = tblTeamDictionary.originalName ")
    cursor.execute(sql)
    conn.commit()
    sql = ("UPDATE ForebetOdds SET AwayTeam = tblTeamDictionary.CorrectName FROM "
           "tblTeamDictionary WHERE trim(ForebetOdds.AwayTeam) = tblTeamDictionary.originalName")
    cursor.execute(sql)
    sql = ("UPDATE PredictzOdds SET HomeTeam = tblTeamDictionary.CorrectName FROM "
           "tblTeamDictionary WHERE trim(PredictzOdds.HomeTeam) = tblTeamDictionary.originalName ")
    cursor.execute(sql)
    sql = ("UPDATE PredictzOdds SET AwayTeam = tblTeamDictionary.CorrectName FROM "
           "tblTeamDictionary WHERE trim(PredictzOdds.AwayTeam) = tblTeamDictionary.originalName")
    cursor.execute(sql)
    conn.commit()
    conn.close()
