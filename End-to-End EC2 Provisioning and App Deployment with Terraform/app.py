from flask import Flask, render_template, request

app = Flask(__name__)

board = [""] * 9
current_player = "X"

@app.route("/", methods=["GET", "POST"])
def game():
    global board, current_player
    if request.method == "POST":
        cell = int(request.form["cell"])
        if board[cell] == "":
            board[cell] = current_player
            current_player = "O" if current_player == "X" else "X"
    return render_template("index.html", board=board)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

