from flask import Flask, send_file
import threading
from squelette_code_python import game
import logging

app = Flask(__name__)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

# Statut du jeu
game_status = "Lancer le jeu ?"
# Score final
final_score = 0
# é
# eviter de lancer plusieur parties en meme temps
game_thread = None

@app.route("/")
def index():
    return send_file("site_projo.html")

def run_game():
    """Exécute le jeu et met à jour le statut et le score final"""
    global game_status, final_score
    game_status = "Jeu en cours"
    score = game()
    final_score = score
    game_status = f"PERDU ! — score : {score}"

@app.route("/start")
def start():
    """Lancer le jeu via un thread pour ne pas bloquer Flask"""
    global game_thread
    if game_thread is None or not game_thread.is_alive():
        game_thread = threading.Thread(target=run_game)
        game_thread.start()
    return "ok"

@app.route("/status")
def status():
    """Renvoie le statut actuel du jeu"""
    return game_status

@app.route("/score")
def score_route():
    """Renvoie le score final"""
    return str(final_score)

@app.route("/css-site.css")
def css():
    return send_file("css-site.css")

@app.route("/pierre-augustine.gif")
def pigeon_gif():
    return send_file("pierre-augustine.gif")

@app.route("/simon.gif")
def simon_gif():
    return send_file("simon.gif")

if __name__ == "__main__":
    app.run(debug=True)
