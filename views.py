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


def player_stats_page(player_ID):
    myDB = current_app.config["dbconfig"]
    player_name = myDB.get_player_name(player_ID)
    return render_template("player_stats.html", player_name=player_name, player_ID=player_ID)


def pitchings_page(playerID, page_num):
    myDB = current_app.config["dbconfig"]
    pitchings = myDB.get_pitchings_by_playerID(playerID, page_num)
    num_of_pages = ceil(myDB.get_num_of_pitchings_by_playerID(playerID) / 10)
    return render_template("pitchings.html", pitchings=pitchings, cur_page=int(page_num), num_of_pages=num_of_pages)


def pitchings_detail_page(playerID, page_num):
    myDB = current_app.config["dbconfig"]
    pitchings = myDB.get_pitchings_detail_by_playerID(playerID, page_num)
    num_of_pages = ceil(myDB.get_num_of_pitchings_by_playerID(playerID) / 10)
    return render_template("pitchings_detail.html", pitchings=pitchings, cur_page=int(page_num), num_of_pages=num_of_pages)


def delete_pitching(page_num, playerID, yearID, stint):
    myDB = current_app.config["dbconfig"]
    myDB.delete_pitching(playerID, yearID, stint)
    return redirect(url_for('pitchings_page', page_num=page_num, playerID=playerID))


def add_pitching(page_num):
    error = 'False'
    if request.method == "POST":
        myDB = current_app.config["dbconfig"]

        playerID_new = request.form.get("playerID")
        yearID_new = request.form.get("yearID")
        stint_new = request.form.get("stint")
        teamID_new = request.form.get("teamID")
        lgID_new = request.form.get("lgID")
        w_new = request.form.get("w")
        l_new = request.form.get("l")

        try:
            new_pitching = Pitching(playerID_new, yearID_new, stint_new, teamID_new, lgID_new, w_new,
                                    l_new)

            myDB.add_pitching(new_pitching)

        except:
            error = 'True'

    return redirect(url_for('pitchings_page', page_num=page_num))


def update_pitching(page_num):
    error = 'False'
    if request.method == "POST":
        myDB = current_app.config["dbconfig"]

        playerID_updated = request.form.get("playerID")
        yearID_updated = request.form.get("yearID")
        stint_updated = request.form.get("stint")
        teamID_updated = request.form.get("teamID")
        lgID_updated = request.form.get("lgID")
        w_updated = request.form.get("w")
        l_updated = request.form.get("l")
        try:
            updated_pitching = Pitching(playerID_updated, yearID_updated, stint_updated, teamID_updated,
                                        lgID_updated, w_updated, l_updated)

            myDB.update_pitching(updated_pitching)

        except:
            error = 'True'

    return redirect(url_for('pitchings_page', page_num=page_num, playerID=playerID_updated))
