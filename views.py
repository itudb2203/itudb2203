from flask import render_template, current_app, request, redirect, url_for
from math import ceil
from batting import Batting

def home_page():
    return render_template("home.html")

def players_page(page_num):
    myDB = current_app.config["dbconfig"]
    players_list = myDB.get_players(page_num)
    num_of_pages = ceil(myDB.get_num_players() / 10)
    return render_template("players.html", players=players_list, cur_page = int(page_num), num_pages = num_of_pages)

def player_stats_page(playerID):
    myDB = current_app.config["dbconfig"]
    player_name = myDB.get_player_name(playerID)
    return render_template("player_stats.html", player_name=player_name, playerID=playerID)

def batting_page(playerID):
    myDB = current_app.config["dbconfig"]
    player_name = myDB.get_player_name(playerID)
    bat = myDB.get_batting(playerID)
    return render_template("batting.html", player_name=player_name, playerID=playerID, batting=bat )

def del_batting(playerID, yearid):
    myDB = current_app.config["dbconfig"]
    myDB.del_batting(playerID, yearid)
    return batting_page(playerID)

def update_batting(playerID, yearid, teamID):
    error = 'False'
    if request.method == "POST":
        myDB = current_app.config["dbconfig"]

        yearid_updated = request.form.get("yearid")
        teamID_updated = request.form.get("teamID")
        lgID = request.form.get("lgID")
        R_updated = request.form.get("R")
        G_updated = request.form.get("G")
        try:
            updated_batting = Batting(playerID,yearid_updated,teamID_updated,lgID,R_updated,G_updated)

            myDB.update_batting(playerID, yearid, teamID, updated_batting)
        except:
            error = 'True'

    return redirect(url_for('batting_page', playerID=playerID, error=error))


def add_batting(playerID):
    error = 'False'
    if request.method == "POST":
        myDB = current_app.config["dbconfig"]

        yearid_new = request.form.get("yearid")
        teamID_new = request.form.get("teamID")
        lgID_new = request.form.get("lgID")
        R_new = request.form.get("R")
        G_new = request.form.get("G")
        try:

            new_BaT = Batting(playerID, yearid_new, teamID_new, lgID_new, R_new, G_new)
            myDB.add_batting(playerID, new_BaT)
        except:
            error = 'True'

    return redirect(url_for('batting_page', playerID=playerID, error=error))