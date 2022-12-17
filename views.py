from flask import render_template, current_app, request, redirect, url_for
from math import ceil

from hall_of_fame import HallOfFame
from player import Player

def home_page():
    return render_template("home.html")


def players_page(page_num, error):
    myDB = current_app.config["dbconfig"]
    players_list = myDB.get_players(page_num)
    num_of_pages = ceil(myDB.get_num_players() / 10) # Every page shows 10 players, #pages is : #players / 10
    return render_template("players.html", players=players_list, cur_page=int(page_num), num_pages=num_of_pages,
                           error=error)

# This page includes hyperlinks to stats pages (appearances, batting, fielding, pitching, hall of fame)
def player_stats_page(playerID):
    myDB = current_app.config["dbconfig"]
    player_name = myDB.get_player_name(playerID)
    return render_template("player_stats.html", player_name=player_name, playerID=playerID)


def del_player(page_num, playerID):
    myDB = current_app.config["dbconfig"]
    myDB.del_player(playerID)
    return redirect(url_for('players_page', page_num=page_num, error='False'))


def update_player(page_num, playerID):
    error = 'False'  # Error message is not displayed if there's no exception
    if request.method == "POST":
        myDB = current_app.config["dbconfig"]
        
        nameFirst_updated = request.form.get("nameFirst")
        nameLast_updated = request.form.get("nameLast")
        birthYear_updated = request.form.get("birthYear")
        birthCountry_updated = request.form.get("birthCountry")
        weight_updated = request.form.get("weight")
        height_updated = request.form.get("height")
        try:
            updated_player = Player(playerID, nameFirst_updated, nameLast_updated, birthYear_updated,
                                    birthCountry_updated, weight_updated, height_updated)

            myDB.update_player(playerID, updated_player)

        except:
            error = 'True'

    return redirect(url_for('players_page', page_num=page_num, error=error))


def add_player(page_num):
    error = 'False'  # Error message is not displayed if there's no exception
    if request.method == "POST":
        myDB = current_app.config["dbconfig"]

        nameFirst_new = request.form.get("nameFirst")
        nameLast_new = request.form.get("nameLast")
        birthYear_new = request.form.get("birthYear")
        birthCountry_new = request.form.get("birthCountry")
        weight_new = request.form.get("weight")
        height_new = request.form.get("height")

        # We will autogenerate id for the new player.
        # PlayerID format : last name's first 5 letter (if less, take the whole string) + first name's first 2 letter + index
        # It's in lower case. index has a length of 2. If it's a single digit integer, there's a 0 in the front.
        # Index is incremented if there exists a player with the same id
        id_lname_len = min(4, len(nameLast_new))  # Length of last name's part in the id
        id_fname_len = min(2, len(nameFirst_new))  # Length of first name's part in the id
        id_lname = nameLast_new[:id_lname_len]  # Last name's part in the id
        id_fname = nameFirst_new[:id_fname_len]  # First name's part in the id

        id_str = (id_lname + id_fname).lower()  # Id without index
        id_ind = 1  # Index part of id

        try:
            while True:
                playerID_new = id_str + f'{id_ind:02d}'  # Append the index to string part to get the player

                if (myDB.check_player(playerID_new) == 0):  # Check if there's a player with same id
                    break  # If there's no player with the same id, use that id
                else:
                    id_ind += 1  # If there's continue increasing index

            new_player = Player(playerID_new, nameFirst_new, nameLast_new, birthYear_new, birthCountry_new, weight_new,
                                height_new)

            myDB.add_player(new_player)
            
        except:
            error = 'True'
            
    return redirect(url_for('players_page', page_num=page_num, error=error))


def hall_of_fame_page(playerID, error):
    myDB = current_app.config["dbconfig"]
    player_name = myDB.get_player_name(playerID)
    hof = myDB.get_hall_of_fame(playerID)
    return render_template("hall_of_fame.html", player_name=player_name, playerID=playerID, hall_of_fame=hof, error=error)


def del_hall_of_fame(playerID, yearid, votedBy):
    myDB = current_app.config["dbconfig"]
    myDB.del_hall_of_fame(playerID, yearid, votedBy) # Primary key for hall of fame is (playerID, yearid, votedBy)
    return redirect(url_for('hall_of_fame_page', playerID=playerID, error='False'))


def update_hall_of_fame(playerID, yearid, votedBy):
    error = 'False'
    if request.method == "POST":
        myDB = current_app.config["dbconfig"]
        
        yearid_updated = request.form.get("yearid")
        category_updated = request.form.get("category")
        votedBy_updated = request.form.get("votedBy")
        ballots_updated = request.form.get("ballots")
        needed_updated = request.form.get("needed")
        votes_updated = request.form.get("votes")

        try:
            # Calculate inducted by comparing needed votes and received votes
            inducted_updated = "N" if int(votes_updated) < int(needed_updated) else "Y"

            if (int(ballots_updated) < int(needed_updated)) or (int(ballots_updated) < int(votes_updated)):
                raise Exception

            updated_hof = HallOfFame(yearid_updated, votedBy_updated, ballots_updated, needed_updated, votes_updated, inducted_updated, category_updated)

            myDB.update_hall_of_fame(playerID, yearid, votedBy, updated_hof)

        except:
            error = 'True'
        return redirect(url_for('hall_of_fame_page', playerID=playerID, error=error))


def add_hall_of_fame(playerID):
    error = 'False'
    if request.method == "POST":
        myDB = current_app.config["dbconfig"]

        yearid_new = request.form.get("yearid")
        category_new = request.form.get("category")
        votedBy_new = request.form.get("votedBy")
        ballots_new = request.form.get("ballots")
        needed_new = request.form.get("needed")
        votes_new = request.form.get("votes")
        
        try:
            inducted_new = "N" if int(votes_new) < int(needed_new) else "Y"

            if (int(ballots_new) < int(needed_new)) or (int(ballots_new) < int(votes_new)):
                raise Exception

            new_hof = HallOfFame(yearid_new, votedBy_new, ballots_new, needed_new, votes_new, inducted_new, category_new)

            myDB.add_hall_of_fame(playerID, new_hof)

        except:
            error = 'True'
            
    return redirect(url_for('hall_of_fame_page', playerID=playerID, error=error))
