from flask import Flask, send_file ,request, jsonify
import threading
from code_simon import game
from database import init_db, add_score, get_scores
import logging


app = Flask(__name__)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

current_score = 0
final_score = 0
game_thread = None
game_over = False

init_db()

@app.route("/")
def index():
    return send_file("site_projo.html")

def run_game():
    global game_over, current_score, final_score

    game_over = False
    current_score = 0

    def update_score(score):
        global current_score
        current_score = score #score mis à jour en live

    final_score = game(update_score)
    game_over = True


@app.route("/start")
def start():
    global game_thread
    if game_thread is None or not game_thread.is_alive():
        game_thread = threading.Thread(target=run_game)
        game_thread.start()
    return "ok"

@app.route("/score")
def score():
    return str(current_score)

@app.route("/save_score", methods=["POST"])
def save_score():
    name = request.form.get("name")
    if name:
        add_score(name, final_score)
    return "ok"

@app.route("/game_over")
def is_game_over():
    return "1" if game_over else "0"


@app.route("/scores")
def scores():
    return jsonify(get_scores())

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
