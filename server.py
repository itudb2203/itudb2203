from flask import Flask
import os

import views
from database import Database


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)

    # Players page url's
    app.add_url_rule("/players/<page_num>", view_func=views.players_page)
    app.add_url_rule("/players/<page_num>/error:<error>", view_func=views.players_page)
    app.add_url_rule("/players/<page_num>/delete/<playerID>", view_func=views.del_player)
    app.add_url_rule("/players/<page_num>/update/<playerID>", methods=["GET", "POST"], view_func=views.update_player)
    app.add_url_rule("/players/<page_num>/add", methods=["GET", "POST"], view_func=views.add_player)

    # Player stats page url
    app.add_url_rule("/player/<playerID>", view_func=views.player_stats_page)

    # Hall of fame page url's
    app.add_url_rule("/player/<playerID>/hall-of-fame/error:<error>", view_func=views.hall_of_fame_page)
    app.add_url_rule("/player/<playerID>/hall-of-fame/delete/<yearid>/<votedBy>", view_func=views.del_hall_of_fame)
    app.add_url_rule("/player/<playerID>/hall-of-fame/update/<yearid>/<votedBy>", methods=["GET", "POST"], view_func=views.update_hall_of_fame)
    app.add_url_rule("/player/<playerID>/hall-of-fame/add", methods=["GET", "POST"], view_func=views.add_hall_of_fame)

    # Teams page url's
    app.add_url_rule("/teams/<page_num>/", view_func=views.teams_page)
    app.add_url_rule("/teams/<page_num>/error:<error>", view_func=views.teams_page)
    app.add_url_rule("/teams/<page_num>/delete/<teamID>", view_func=views.del_team)
    app.add_url_rule("/teams/<page_num>/update/<teamID>", methods=["GET", "POST"], view_func=views.update_team)
    app.add_url_rule("/teams/<page_num>/add", methods=["GET", "POST"], view_func=views.add_team)

    home_dir = os.getcwd()

    db = Database(os.path.join(home_dir, "lahman2016.sqlite"))

    app.config["dbconfig"] = db

    return app

if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)


