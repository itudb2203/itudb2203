from flask import render_template, current_app, request
from math import ceil

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

def hall_of_fame_page(player_ID):
    myDB = current_app.config["dbconfig"]
    player_name = myDB.get_player_name(player_ID)
    hof = myDB.get_hall_of_fame(player_ID)
    return render_template("hall_of_fame.html", player_name=player_name, player_ID=player_ID, hall_of_fame=hof)

def del_hall_of_fame(player_ID, yearid):
    myDB = current_app.config["dbconfig"]
    myDB.del_hall_of_fame(player_ID, yearid)
    return hall_of_fame_page(player_ID)


def update_hall_of_fame(player_ID, yearid):
    if request.method == "POST":
        yearidForm = request.form.get("yearidUpdate")
        categoryForm = request.form.get("categoryUpdate")
        votedByForm = request.form.get("votedByUpdate")
        ballotsForm = request.form.get("ballotsUpdate")
        neededForm = request.form.get("neededUpdate")
        votesForm = request.form.get("votesUpdate")

        print(yearid)
        print(yearidForm)
        print(categoryForm)
        print(votedByForm)
        print(ballotsForm)
        print(neededForm)
        print(votesForm)

    return hall_of_fame_page(player_ID)

