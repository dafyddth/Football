import sqlite3

prem_teams = {
    "Arsenal": "Arsenal",
    "Aston Villa": "Aston Villa",
    "Bournemouth": "Bournemouth",
    "Brentford": "Brentford",
    "Brighton & Hove Albion": "Brighton",
    "Chelsea": "Chelsea",
    "Crystal Palace": "Crystal Palace",
    "Everton": "Everton",
    "Fulham": "Fulham",
    "Ipswich Town": "Ipswich",
    "Leicester City": "Leicester",
    "Liverpool": "Liverpool",
    "Manchester City": "Manchester City",
    "Manchester United": "Manchester United",
    "Newcastle United": "Newcastle United",
    "Nottingham Forest": "Nottingham Forest",
    "Southampton": "Southampton",
    "Tottenham Hotspur": "Tottenham",
    "West Ham United": "West Ham",
    "Wolves": "Wolves",
    "Brighton": "Brighton",
    "Leicester": "Leicester",
    "Ipswich": "Ipswich",
    "Tottenham": "Tottenham",
    "Spurs": "Tottenham",
    "West Ham": "West Ham"
    }
conn = sqlite3.connect('Football.db')
cursor = conn.cursor()
conn.execute("CREATE TABLE IF NOT EXISTS tblTeamDictionary (ID Integer PRIMARY KEY, originalName Text, correctName Text);")
conn.commit()
conn.execute("DELETE FROM tblTeamDictionary")
conn.commit()
for key in prem_teams.keys():
    sql = f"INSERT INTO tblTeamDictionary(originalName, correctName) VALUES('{key}','{prem_teams.get(key)}');"
    cursor.execute(sql)
conn.commit()