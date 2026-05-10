from flask import Flask, jsonify, request
import random

app = Flask(__name__)

players = [
    "Player1",
    "Player2",
    "Player3",
    "Player4"
]

roles = {}

scores = {
    "Player1": 0,
    "Player2": 0,
    "Player3": 0,
    "Player4": 0
}

round_history = []

round_no = 1

MAX_ROUNDS = 5


@app.route("/start-round")
def start_round():

    global roles
    global round_no

    role_list = [
        "BABU",
        "CHOR",
        "POLICE",
        "DAKAT"
    ]

    random.shuffle(role_list)

    roles = dict(zip(players, role_list))

    babu_player = ""
    police_player = ""

    for player, role in roles.items():

        if role == "BABU":
            babu_player = player
            scores[player] += 1000

        if role == "POLICE":
            police_player = player

    return jsonify({
        "roles": roles,
        "babu": babu_player,
        "police": police_player,
        "round": round_no
    })


@app.route("/guess", methods=["POST"])
def guess():

    global round_no

    data = request.json

    chor_guess = data["chor"]
    dakat_guess = data["dakat"]

    actual_chor = ""
    actual_dakat = ""
    police_player = ""

    for player, role in roles.items():

        if role == "CHOR":
            actual_chor = player

        elif role == "DAKAT":
            actual_dakat = player

        elif role == "POLICE":
            police_player = player

    result = "wrong"

    if (
        chor_guess == actual_chor and
        dakat_guess == actual_dakat
    ):

        scores[police_player] += 500
        result = "correct"

    else:

        scores[actual_chor] += 400
        scores[actual_dakat] += 600

    round_history.append({
        "round": round_no,
        "babu": [
            p for p, r in roles.items()
            if r == "BABU"
        ][0],
        "police": police_player,
        "chor": actual_chor,
        "dakat": actual_dakat,
        "result": result
    })

    round_no += 1

    winner = None

    if round_no > MAX_ROUNDS:

        winner = max(
            scores,
            key=scores.get
        )

    return jsonify({
        "result": result,
        "actual_chor": actual_chor,
        "actual_dakat": actual_dakat,
        "scores": scores,
        "history": round_history,
        "winner": winner,
        "game_over": round_no > MAX_ROUNDS
    })


@app.route("/reset", methods=["POST"])
def reset():

    global scores
    global round_history
    global round_no

    scores = {
        "Player1": 0,
        "Player2": 0,
        "Player3": 0,
        "Player4": 0
    }

    round_history = []

    round_no = 1

    return jsonify({
        "message": "Game Reset"
    })


if __name__ == "__main__":

    app.run(
        debug=False,
        host="0.0.0.0",
        port=5000
    )