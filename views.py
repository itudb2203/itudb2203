from flask import render_template, current_app, request, redirect, url_for
from math import ceil
from batting import Batting
from appearances import Appearances


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


def batting_page(playerID,error):
    myDB = current_app.config["dbconfig"]
    player_name = myDB.get_player_name(playerID)
    bat = myDB.get_batting(playerID)
    return render_template("batting.html", player_name=player_name, playerID=playerID, batting=bat , error = error)


def appearances_page(playerID,error):
    myDB = current_app.config["dbconfig"]
    player_name = myDB.get_player_name(playerID)
    app = myDB.get_appearances(playerID)
    return render_template("appearances.html", player_name=player_name, playerID=playerID, appearances=app , error = error)


def del_batting(playerID, yearid):
    myDB = current_app.config["dbconfig"]
    error = 'False'
    myDB.del_batting(playerID, yearid)
    return redirect(url_for('batting_page', playerID=playerID, error=error))

def update_batting(playerID, yearid, teamID):
    error = 'False'
    if request.method == "POST":
        myDB = current_app.config["dbconfig"]
        yearid_updated = request.form.get("yearid")
        teamID_updated = request.form.get("teamID")
        lgID = request.form.get("lgID")
        R_updated = request.form.get("R")
        G_updated = request.form.get("G")
        if yearid_updated.isdigit() == False:
            error = "True"
        if teamID_updated.isdigit() == True:
            error = "True"
        if lgID.isdigit() == True:
            error = "True"
        if R_updated.isdigit() == False:
            error = "True"
        if G_updated.isdigit() == False:
            error = "True"
        print(yearid_updated)
        print(teamID_updated)
        print(lgID)
        print(R_updated)
        print(G_updated)
        if error == "False":
            updated_batting = Batting(yearid_updated,teamID_updated,lgID,R_updated,G_updated,0,0,0)

            myDB.update_batting(playerID, yearid, teamID, updated_batting)
        else:
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
        if yearid_new.isdigit() == False:
            error = "True"
        if teamID_new.isdigit() == True:
            error = "True"
        if lgID_new.isdigit() == True:
            error = "True"
        if R_new.isdigit() == False:
            error = "True"
        if G_new.isdigit() == False:
            error = "True"
        if error == "False":

            new_BaT = Batting(yearid_new, teamID_new, lgID_new, R_new, G_new , 0 , 0 , 0)
            myDB.add_batting(playerID, new_BaT)
        else:
            error = 'True'

    return redirect(url_for('batting_page', playerID=playerID, error=error))

def del_appearances(playerID, yearid):
    myDB = current_app.config["dbconfig"]
    myDB.del_appearances(playerID, yearid)
    error = "False"
    return redirect(url_for('appearances_page', playerID=playerID, error=error))




def update_appearances(playerID, yearid, teamID):
    error = 'False'
    if request.method == "POST":
        myDB = current_app.config["dbconfig"]
        yearid_updated = request.form.get("yearid")
        teamID_updated = request.form.get("teamID")
        lgID_updated = request.form.get("lgID")
        GS_updated = request.form.get("GS")
        G_batting_updated = request.form.get("G_batting")
        G_p_updated = request.form.get("G_p")
        if yearid_updated.isdigit() == False:
            error = "True"
        if teamID_updated.isdigit() == True:
            error = "True"
        if lgID_updated.isdigit() == True:
            error = "True"
        if GS_updated.isdigit() == False:
            error = "True"
        if G_batting_updated.isdigit() == False:
            error = "True"
        if G_p_updated.isdigit() == False:
            error = "True"

        if error == "False":
            updated_batting = Appearances(yearid_updated,teamID_updated,lgID_updated,playerID ,GS_updated,G_batting_updated,G_p_updated)

            myDB.update_appearances(playerID, yearid, teamID, updated_batting)
        else:
            error = 'True'

    return redirect(url_for('appearances_page', playerID=playerID, error=error))


def add_appearances(playerID):
    error = 'False'
    if request.method == "POST":
        myDB = current_app.config["dbconfig"]

        yearid_new = request.form.get("yearid")
        teamID_new = request.form.get("teamID")
        lgID_new = request.form.get("lgID")
        GS_new = request.form.get("GS")
        G_batting_new = request.form.get("G_batting")
        G_p_new = request.form.get("G_p")
        if yearid_new.isdigit() == False:
            error = "True"
        if teamID_new.isdigit() == True:
            error = "True"
        if lgID_new.isdigit() == True:
            error = "True"
        if GS_new.isdigit() == False:
            error = "True"
        if G_batting_new.isdigit() == False:
            error = "True"
        if G_p_new.isdigit() == False:
            error = "True"

        if error == "False":

            new_App = Appearances(yearid_new, teamID_new, lgID_new, playerID , GS_new, G_batting_new ,G_p_new)
            myDB.add_appearances(playerID, new_App)
        else:
            error = 'True'

    return redirect(url_for('appearances_page', playerID=playerID, error=error))