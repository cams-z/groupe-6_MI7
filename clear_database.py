import sqlite3

DB_NAME = "scores.db"

def clear_scores():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM scores")
    conn.commit()
    conn.close()
    print("Base de données vidée avec succès.")

if __name__ == "__main__":
    clear_scores()
