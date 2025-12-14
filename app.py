from flask import Flask, send_file
import threading
from squelette_code_python import game
import logging

app = Flask(__name__)

logging.getLogger('werkzeug').setLevel(logging.ERROR)

game_status = "En attente"

@app.route("/")
def index():
    return send_file("site_projo.html")

@app.route("/start")
def start():
    global game_status
    game_status = "Jeu en cours"
    threading.Thread(target=run_game).start()
    return "ok"


def run_game():
    global game_status
    score = game()
    game_status = f"Perdu — score : {score}"

@app.route("/status")
def status():
    return game_status

@app.route("/css-site.css")
def css():
    return send_file("css-site.css")

@app.route("/pierre-augustine.gif")
def img():
    return send_file("pierre-augustine.gif")

if __name__ == "__main__":
    app.run(debug=True)
