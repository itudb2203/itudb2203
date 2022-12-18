import sqlite3 as dbapi2
from pitching import Pitching
from player import Player


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
                players_list.append(
                    Player(playerID, nameFirst, nameLast, birthYear, birthCountry, weight, height))
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

    def get_player_name(self, playerID):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """SELECT nameFirst, nameLast FROM Master
            WHERE playerID = ?"""
            cursor.execute(query, (playerID,))
            name_list = cursor.fetchone()
            cursor.close()
            return name_list[0] + " " + name_list[1]

    def get_pitchings_by_playerID(self, playerID):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """SELECT playerID, yearID, teamID, lgID, W, L, H FROM Pitching
            WHERE playerID = ?"""
            cursor.execute(query, (playerID,))
            pitchings = []
            for playerID, yearID, teamID, lgID, w, l, h in cursor:
                pitchings.append(
                    Pitching(playerID, yearID, teamID, lgID, w, l, h))
            cursor.close()
            return pitchings

    def delete_pitching(self, playerID, yearID):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM Pitching
            WHERE playerID = ? AND yearID = ?"""
            cursor.execute(query, (playerID, yearID))
            cursor.close()

    def add_pitching(self, pitching):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO Pitching 
            (playerID, yearid, teamID, lgID, W, L, H)
            VALUES (?,?,?,?,?,?,?)"""
            cursor.execute(query, (pitching.playerID, pitching.yearID,
                           pitching.teamID, pitching.lgID, pitching.w, pitching.l, pitching.hits))
            cursor.close()

    def update_pitching(self, pitching, playerID, yearID):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """UPDATE Pitching
            SET teamID = ?, lgID =? ,w=?, l=?, yearid = ?, h=?
            WHERE playerID = ? AND yearID = ?"""
            cursor.execute(query, (pitching.teamID, pitching.lgID,
                           pitching.w, pitching.l, pitching.yearID, pitching.hits,playerID, yearID))
            cursor.close()
