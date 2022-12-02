from flask import Flask
import os

import views
from database import Database


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/players/<page_num>", view_func=views.players_page)
    app.add_url_rule("/player/<player_ID>", view_func=views.player_stats_page)
    app.add_url_rule("/player/<player_ID>/hall-of-fame", view_func=views.hall_of_fame_page)

    home_dir = os.getcwd()

    db = Database(os.path.join(home_dir, "lahman2016.sqlite"))

    app.config["dbconfig"] = db

    return app

if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)


