import sqlite3 as dbapi2
from pitching import Pitching
from pitchingDetail import PitchingDetail
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

    def get_player_name(self, player_ID):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """SELECT nameFirst, nameLast FROM Master
            WHERE playerID = ?"""
            cursor.execute(query, (player_ID,))
            name_list = cursor.fetchone()
            cursor.close()
            return name_list[0] + " " + name_list[1]

    def get_pitchings_by_playerID(self, playerID, page_num):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """SELECT playerID, yearID, stint, teamID, lgID, W, L FROM Pitching
            WHERE playerID = ?
            LIMIT 10 OFFSET ?"""
            cursor.execute(query, (playerID, (int(page_num) - 1) * 10,))
            pitchings = []
            for playerID, yearID, stint, teamID, lgID, W, L in cursor:
                pitchings.append(
                    Pitching(playerID, yearID, stint, teamID, lgID, W, L))
            cursor.close()
            return pitchings

    def get_pitchings_detail_by_playerID(self, playerID, page_num):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """SELECT playerID, Pitching.yearID, stint, name, Pitching.lgID, Pitching.W, Pitching.L FROM Pitching
            JOIN Teams ON Pitching.teamID=Teams.teamID
            WHERE playerID = ?
            LIMIT 10 OFFSET ?"""
            cursor.execute(query, (playerID, (int(page_num) - 1) * 10,))
            pitchings = []
            for playerID, yearID, stint, name, lgID, W, L in cursor:
                pitchings.append(
                    PitchingDetail(playerID, yearID, stint, name, lgID, W, L))
            cursor.close()
            return pitchings

    def get_num_of_pitchings_by_playerID(self, playerID):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """SELECT COUNT (*) FROM Pitching AS num_of_pitchings
            WHERE playerID = ?"""
            cursor.execute(query, (playerID,))
            num_of_pitchings = cursor.fetchone()[0]
            cursor.close()
            return num_of_pitchings

    def delete_pitching(self, playerID, yearID, stint):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM Pitching
            WHERE playerID = ? AND yearID = ? AND stint = ?"""
            cursor.execute(query, (playerID, yearID, stint,))
            query = """UPDATE Pitching SET stint = stint - 1
            WHERE playerID=? AND yearID=? AND stint>?"""
            cursor.execute(query, (playerID, yearID, stint,))
            cursor.close()
            # self.update_stints_on_delete(playerID, yearID, stint)

    def get_stint(self, playerID, yearID):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """SELECT stint FROM Pitching
            WHERE playerID=? and yearID=?
            ORDER BY DESC stint"""
            cursor.execute(query, (playerID, yearID,))
            stint = cursor.fetchone()[0]
            cursor.close()
            return stint

    def update_stints_on_delete(self, playerID, yearID, stint):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """UPDATE Pitching SET stint = stint - 1
            WHERE playerID=? AND yearID=? AND stint>?"""
            cursor.execute(query, (playerID, yearID, stint,))
            cursor.close()

    def add_pitching(self, pitching):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO Pitching 
            (playerID, yearid, stint, teamID, lgID, W, L)
            VALUES (?, ?,?,?,?,?,? )"""
            stint = self.get_stint(pitching.playerID, pitching.yearID)
            cursor.execute(query, (pitching.playerID, pitching.yearID, stint,
                           pitching.teamID, pitching.lgID, pitching.w, pitching.l,))
            cursor.close()

    def update_pitching(self, pitching):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """UPDATE Pitching
            SET stint = ?, teamID = ?, lgID =? ,w=?, l=?
            WHERE playerID = ?, yearid = ?"""
            cursor.execute(query, (pitching.stint, pitching.teamID, pitching.lgID,
                           pitching.w, pitching.l, pitching.playerID, pitching.yearID,))
            cursor.close()
