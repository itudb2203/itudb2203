from flask import render_template, current_app, request, redirect, url_for
from math import ceil
from hall_of_fame import HallOfFame

def home_page():
    return render_template("home.html")

def players_page(page_num):
    myDB = current_app.config["dbconfig"]
    players_list = myDB.get_players(page_num)
    num_of_pages = ceil(myDB.get_num_players() / 10)
    return render_template("players.html", players=players_list, cur_page = int(page_num), num_pages = num_of_pages)

def player_stats_page(player_ID):
    myDB = current_app.config["dbconfig"]
    player_name = myDB.get_player_name(player_ID)
    return render_template("player_stats.html", player_name=player_name, player_ID=player_ID)

def hall_of_fame_page(player_ID, error):
    myDB = current_app.config["dbconfig"]
    player_name = myDB.get_player_name(player_ID)
    hof = myDB.get_hall_of_fame(player_ID)
    return render_template("hall_of_fame.html", player_name=player_name, player_ID=player_ID, hall_of_fame=hof, error=error)

def del_hall_of_fame(player_ID, yearid, votedBy):
    myDB = current_app.config["dbconfig"]
    myDB.del_hall_of_fame(player_ID, yearid, votedBy)
    return redirect(url_for('hall_of_fame_page', player_ID=player_ID, error=False))

def update_hall_of_fame(player_ID, yearid, votedBy):
    error = False
    if request.method == "POST":
        myDB = current_app.config["dbconfig"]

        yearid_updated = request.form.get("yearid")
        category_updated = request.form.get("category")
        votedBy_updated = request.form.get("votedBy")
        ballots_updated = request.form.get("ballots")
        needed_updated = request.form.get("needed")
        votes_updated = request.form.get("votes")
        try:
            inducted_updated = "N" if int(votes_updated) < int(needed_updated) else "Y"

            updated_hof = HallOfFame(yearid_updated, votedBy_updated, ballots_updated, needed_updated, votes_updated, inducted_updated, category_updated)

            myDB.update_hall_of_fame(player_ID, yearid, votedBy, updated_hof)
        except:
            error = True

    return redirect(url_for('hall_of_fame_page', player_ID=player_ID, error=error))

def add_hall_of_fame(player_ID):
    error = False
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

            new_hof = HallOfFame(yearid_new, votedBy_new, ballots_new, needed_new, votes_new, inducted_new, category_new)

            myDB.add_hall_of_fame(player_ID, new_hof)
        except:
            error = True

    return redirect(url_for('hall_of_fame_page', player_ID=player_ID, error=error))