from flask import render_template, current_app
from math import ceil


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
