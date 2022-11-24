from flask import render_template, current_app
from math import ceil

def home_page():
    return render_template("home.html")

def players_page(page_num):
    myDB = current_app.config["dbconfig"]
    players_list = myDB.get_players(page_num)
    num_of_pages = ceil(myDB.get_num_players() / 10)
    return render_template("players.html", players=players_list, cur_page = int(page_num), num_pages = num_of_pages)
def teams_page(page_num):
    myDB = current_app.config["dbconfig"]
    teams_list = myDB.get_teams(page_num)
    num_of_pages = ceil(myDB.get_num_teams() / 10)
    return render_template("teams.html", teams=teams_list, cur_page = int(page_num), num_pages = num_of_pages)