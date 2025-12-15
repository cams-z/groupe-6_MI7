from flask import Flask, send_file
import threading
from squelette_code_python import game
import logging

app = Flask(__name__)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

game_status = "Lancer le jeu ?"
current_score = 0
final_score = 0
game_thread = None

@app.route("/")
def index():
    return send_file("site_projo.html")

def run_game():
    global game_status, current_score, final_score

    current_score = 0
    game_status = "Jeu lancer !"

    def update_score(score):
        global current_score
        current_score = score   # score mis à jour en live

    final_score = game(update_score)
    game_status = f"PERDU !"

@app.route("/start")
def start():
    global game_thread
    if game_thread is None or not game_thread.is_alive():
        game_thread = threading.Thread(target=run_game)
        game_thread.start()
    return "ok"

@app.route("/status")
def status():
    return game_status

@app.route("/score")
def score():
    return str(current_score)

@app.route("/css-site.css")
def css():
    return send_file("css-site.css")

@app.route("/pierre-augustine.gif")
def pigeon():
    return send_file("pierre-augustine.gif")

@app.route("/simon.gif")
def simon():
    return send_file("simon.gif")

if __name__ == "__main__":
    app.run(debug=True)
