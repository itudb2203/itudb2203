import sqlite3 as dbapi2
from player import Player
from batting import Batting


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

    def get_num_players(self):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT COUNT (*) FROM Master AS num_players"
            cursor.execute(query)
            num_of_players = cursor.fetchone()[0]
            cursor.close()
            return num_of_players

    def get_player_name(self,playerID):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """SELECT nameFirst, nameLast FROM Master
            WHERE playerID = ?"""
            cursor.execute(query, (playerID,))
            name_list = cursor.fetchone()
            cursor.close()
            return name_list[0] + " " + name_list[1]

    def get_batting(self, playerID):
        batting_list = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """SELECT yearID, teamID, lgID, R, G ,H,RBI,BB FROM batting
            WHERE playerID = ?
            ORDER BY yearID"""
            cursor.execute(query, (playerID,))
            for yearid, teamID, lgID, R, G ,H,RBI , BB in cursor:
                batting_list.append(Batting(yearid, teamID, lgID, R, G , H , RBI , BB))
            cursor.close()
            return batting_list

    def del_batting(self, playerID, yearid):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM batting WHERE (playerID = ? AND yearID = ?)"
            cursor.execute(query, (playerID, yearid))
            cursor.close()

    def update_batting(self, playerID, yearid, teamID, updated_batting):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            print(updated_batting.yearid, updated_batting.teamID, updated_batting.lgID, updated_batting.R, updated_batting.G)
            query = """UPDATE batting
            SET yearID = ?,
                teamID = ?,
                lgID = ?,
                R = ?,
                G = ?,
                H = ?,
                RBI = ?,
                BB = ?
            WHERE
                (playerID = ? AND yearID = ? AND teamID = ?)"""

            cursor.execute(query, (updated_batting.yearid, updated_batting.teamID, updated_batting.lgID, updated_batting.R, updated_batting.G,0,0,0, playerID, yearid, teamID))
            cursor.close()



    def add_batting(self, playerID, new_BaT):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO batting (playerID, yearID, teamID, lgID, R, G , H ,RBI , BB)
            VALUES (?, ?, ?, ?, ?, ? , ? , ? , ?);"""

            cursor.execute(query, (playerID, new_BaT.yearid, new_BaT.teamID, new_BaT.lgID, new_BaT.R, new_BaT.G,0,0,0))
            cursor.close()