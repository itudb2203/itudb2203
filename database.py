import sqlite3 as dbapi2
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

    def del_player(self, playerID):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM Master WHERE playerID = ?"
            cursor.execute(query, (playerID,))
            cursor.close()

    def update_player(self, playerID, updated_player):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """UPDATE Master
            SET playerID = ?,
                nameFirst = ?,
                nameLast = ?,
                birthYear = ?,
                birthCountry = ?,
                weight = ?,
                height = ?
            WHERE
                playerID = ?"""

            cursor.execute(query, (updated_player.playerID, updated_player.nameFirst, updated_player.nameLast, updated_player.birthYear,
                                   updated_player.birthCountry, updated_player.weight, updated_player.height, playerID))
            cursor.close()
    def add_player(self, new_player):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO Master (playerID, nameFirst, nameLast, birthYear, birthCountry, weight, height)
            VALUES (?, ?, ?, ?, ?, ?, ?);"""

            cursor.execute(query, (new_player.playerID, new_player.nameFirst, new_player.nameLast, new_player.birthYear,
                                   new_player.birthCountry, new_player.weight, new_player.height))
            cursor.close()
