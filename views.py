from flask import render_template, current_app, Flask


def home_page():
    return render_template("home.html")


def players_page(page_num):
    myDB = current_app.config["dbconfig"]
    players_list = myDB.get_players(page_num)
    return render_template("players.html", players=players_list, cur_page = int(page_num))


