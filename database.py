import sqlite3 as dbapi2
from player import Player
from team import Team

class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile

    def get_players(self, page_num):
        players_list = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """SELECT playerID, nameFirst, nameLast, birthYear, birthCountry, weight, height FROM Master
            ORDER BY playerID
            LIMIT 10 OFFSET ?"""
            cursor.execute(query, ((int(page_num) - 1) * 10,))
            for playerID, nameFirst, nameLast, birthYear, birthCountry, weight, height in cursor:
                players_list.append(Player(playerID, nameFirst, nameLast, birthYear, birthCountry, weight, height))
            cursor.close()
        return players_list
    def get_teams(self, page_num):
        teams_list = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """SELECT teamID, yearID, name, Rank, LgWin, G, W, L, R, E, park FROM Teams
            ORDER BY teamID,yearID
            LIMIT 10 OFFSET ?"""
            cursor.execute(query, ((int(page_num) - 1) * 10,))
            for teamID, yearID, name, Rank, LgWin, G, W, L, R, E, park in cursor:
                teams_list.append(Team(teamID, yearID, name, Rank, LgWin, G, W, L, R, E, park))
            cursor.close()
        return teams_list
    def get_num_teams(self):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT COUNT (*) FROM Teams AS num_teams"
            cursor.execute(query)
            num_of_teams = cursor.fetchone()[0]
            cursor.close()
            return num_of_teams
    def get_num_players(self):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT COUNT (*) FROM Teams AS num_players"
            cursor.execute(query)
            num_of_players = cursor.fetchone()[0]
            cursor.close()
            return num_of_players
