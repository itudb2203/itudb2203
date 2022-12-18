from flask import render_template, current_app, redirect, request, url_for
from math import ceil

from pitching import Pitching


def home_page():
    return render_template("home.html")


def players_page(page_num):
    myDB = current_app.config["dbconfig"]
    players_list = myDB.get_players(page_num)
    num_of_pages = ceil(myDB.get_num_players() / 10)
    return render_template("players.html", players=players_list, cur_page=int(page_num), num_pages=num_of_pages)


def player_stats_page(playerID):
    myDB = current_app.config["dbconfig"]
    player_name = myDB.get_player_name(playerID)
    return render_template("player_stats.html", player_name=player_name, playerID=playerID)


def pitchings_page(playerID):
    myDB = current_app.config["dbconfig"]
    pitchings = myDB.get_pitchings_by_playerID(playerID)
    return render_template("pitchings.html", playerID=playerID, pitchings=pitchings)


def delete_pitching(playerID, yearID):
    myDB = current_app.config["dbconfig"]
    myDB.delete_pitching(playerID, yearID)
    return redirect(url_for('pitchings_page', playerID=playerID))


def add_pitching(playerID):
    error = 'False'
    if request.method == "POST":
        myDB = current_app.config["dbconfig"]

        yearID_new = request.form.get("yearID")
        teamID_new = request.form.get("teamID")
        lgID_new = request.form.get("lgID")
        w_new = request.form.get("w")
        l_new = request.form.get("l")
        hits_new = request.form.get("hits")
        saves_new = request.form.get("saves")
        games_new = request.form.get("games")

        try:
            new_pitching = Pitching(
                playerID, int(yearID_new), teamID_new, lgID_new, int(w_new), int(l_new), int(hits_new), int(saves_new), int(games_new))

            myDB.add_pitching(new_pitching)

        except:
            error = 'True'

    return redirect(url_for('pitchings_page', playerID=playerID, error=error))


def update_pitching(playerID, yearID):
    error = 'False'
    if request.method == "POST":
        myDB = current_app.config["dbconfig"]

        yearID_updated = request.form.get("yearID")
        teamID_updated = request.form.get("teamID")
        lgID_updated = request.form.get("lgID")
        w_updated = request.form.get("w")
        l_updated = request.form.get("l")
        hits_updated = request.form.get("hits")
        saves_updated = request.form.get("saves")
        games_updated = request.form.get("games")

        try:
            updated_pitching = Pitching(playerID, int(yearID_updated), teamID_updated,
                                        lgID_updated, int(w_updated), int(l_updated), int(hits_updated), int(saves_updated), int(games_updated))

            myDB.update_pitching(updated_pitching, playerID, yearID)

        except:
            error = 'True'

    return redirect(url_for('pitchings_page', playerID=playerID, error=error))
