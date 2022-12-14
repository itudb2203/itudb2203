from flask import render_template, current_app
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

def batting_page(player_ID):
    myDB = current_app.config["dbconfig"]
    player_name = myDB.get_player_name(player_ID)
    bat = myDB.get_batting(player_ID)
    return render_template("batting.html", player_name=player_name, player_ID=player_ID, batting=bat)

def del_batting(player_ID, yearid):
    myDB = current_app.config["dbconfig"]
    myDB.del_batting(player_ID, yearid)
    return batting_page(player_ID)