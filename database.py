import sqlite3 as dbapi2
from player import Player
from team import Team
from hall_of_fame import HallOfFame
from manager import Manager

class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile

    # Get 10 players with offset for players page
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

    # Get # of players to calculate total page number

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

    # Get player name to display it in stats pages (player_stats, appearances, batting, fielding, pitching, hall of fame)
    def get_player_name(self,playerID):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """SELECT nameFirst, nameLast FROM Master
            WHERE playerID = ?"""
            cursor.execute(query, (playerID,))
            name_list = cursor.fetchone()
            cursor.close()
            return name_list[0] + " " + name_list[1]

    # Get hall of fame data of the player to display it in player's hall of fame page
    def get_hall_of_fame(self, playerID):
        hof_list = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """SELECT yearid, votedBy, ballots, needed, votes, inducted, category FROM HallOfFame
            WHERE playerID = ?
            ORDER BY yearid"""
            cursor.execute(query, (playerID,))
            for yearid, votedBy, ballots, needed, votes, inducted, category in cursor:
                hof_list.append(HallOfFame(yearid, votedBy, ballots, needed, votes, inducted, category))
            cursor.close()
            return hof_list

    # Delete specific hall of fame data of the player
    def del_hall_of_fame(self, playerID, yearid, votedBy):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM HallOfFame WHERE (playerID = ? AND yearid = ? AND votedBy = ?)"
            cursor.execute(query, (playerID, yearid, votedBy))
            cursor.close()

    # Update specific hall of fame data of the player
    def update_hall_of_fame(self, playerID, yearid, votedBy, updated_hof):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """UPDATE HallOfFame
            SET yearid = ?,
                votedBy = ?,
                ballots = ?,
                needed = ?,
                votes = ?,
                inducted = ?,
                category = ?
            WHERE
                (playerID = ? AND yearid = ? AND votedBy = ?)"""

            cursor.execute(query, (updated_hof.yearid, updated_hof.votedBy, updated_hof.ballots, updated_hof.needed, updated_hof.votes,
                                   updated_hof.inducted, updated_hof.category, playerID, yearid, votedBy))
            cursor.close()

    # Add new hall of fame data
    def add_hall_of_fame(self, playerID, new_hof):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO HallOfFame (playerID, yearid, votedBy, ballots, needed, votes, inducted, category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""

            cursor.execute(query, (playerID, new_hof.yearid, new_hof.votedBy, new_hof.ballots, new_hof.needed, new_hof.votes,
                                   new_hof.inducted, new_hof.category))
            cursor.close()

    def get_teams(self, page_num):
        teams_list = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """SELECT yearID, lgID, teamID, name, Rank, LgWin, G, W, L, R, E, park FROM Teams
            ORDER BY yearID,lgID,teamID
            LIMIT 10 OFFSET ?"""
            cursor.execute(query, ((int(page_num) - 1) * 10,))
            for yearID, lgID, teamID, name, Rank, LgWin, G, W, L, R, E, park in cursor:
                teams_list.append(Team(yearID, lgID, teamID, name, Rank, LgWin, G, W, L, R, E, park))
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

    def del_team(self, yearID, lgID, teamID):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM Teams WHERE (yearID = ? AND lgID = ? AND teamID = ?)"
            cursor.execute(query, (yearID, lgID, teamID))
            cursor.close()

    def update_team(self, yearID, lgID, teamID, updated_team):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """UPDATE Teams
            SET yearID = ?,
                lgID = ?,
                teamID = ?,
                name = ?,
                Rank = ?,
                LgWin = ?,
                G = ?,
                W = ?,
                L = ?,
                R = ?,
                E = ?,
                park = ?
            WHERE
                (yearID = ? AND lgID = ? AND teamID = ?)"""

            cursor.execute(query, (updated_team.yearID, updated_team.lgID, updated_team.teamID, updated_team.name, updated_team.Rank,
                                   updated_team.LgWin, updated_team.G, updated_team.W, updated_team.L, updated_team.R, updated_team.E, updated_team.park, yearID, lgID, teamID))
            cursor.close()

    def add_team(self, new_team):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO Teams (yearID, lgID, teamID, name, Rank, LgWin, G, W, L, R, E, park)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

            cursor.execute(query, (new_team.yearID, new_team.lgID, new_team.teamID, new_team.name, new_team.Rank,
                                   new_team.LgWin, new_team.G, new_team.W, new_team.L, new_team.R, new_team.E, new_team.park))
            cursor.close()

    def get_managers(self, page_num):
        managers_list = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """SELECT playerID, yearID, teamID, lgID, inseason, G, W, L, rank, plyrMgr FROM Managers
            ORDER BY yearID,teamID,inseason
            LIMIT 10 OFFSET ?"""
            cursor.execute(query, ((int(page_num) - 1) * 10,))
            for playerID, yearID, teamID, lgID, inseason, G, W, L, rank, plyrMgr in cursor:
                managers_list.append(Manager(playerID, yearID, teamID, lgID, inseason, G, W, L, rank, plyrMgr))
            cursor.close()
        return managers_list

    def get_num_managers(self):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT COUNT (*) FROM Managers AS num_managers"
            cursor.execute(query)
            num_of_managers = cursor.fetchone()[0]
            cursor.close()
            return num_of_managers

    def del_manager(self, yearID, teamID, inseason):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM Managers WHERE (yearID = ? AND teamID = ? AND inseason = ?)"
            cursor.execute(query, (yearID, teamID, inseason))
            cursor.close()

    def update_manager(self, yearID, teamID, inseason, updated_manager):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """UPDATE Managers
            SET playerID = ?,
                yearID = ?,
                teamID = ?,
                lgID = ?,
                inseason = ?,
                G = ?,
                W = ?,
                L = ?,
                rank = ?,
                plyrMgr = ?
            WHERE
                (yearID = ? AND teamID = ? AND inseason = ?)"""

            cursor.execute(query, (updated_manager.playerID, updated_manager.yearID, updated_manager.teamID, updated_manager.lgID, updated_manager.inseason,
                                   updated_manager.G, updated_manager.W, updated_manager.L, updated_manager.rank, updated_manager.plyrMgr, yearID, teamID, inseason))
            cursor.close()

    def add_manager(self, new_manager):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO Managers (playerID, yearID, teamID, lgID, inseason, G, W, L, rank, plyrMgr)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

            cursor.execute(query, (new_manager.playerID, new_manager.yearID, new_manager.teamID, new_manager.lgID, new_manager.inseason,
                                   new_manager.G, new_manager.W, new_manager.L, new_manager.rank, new_manager.plyrMgr))
            cursor.close()