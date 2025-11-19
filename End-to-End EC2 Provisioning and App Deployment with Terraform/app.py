from flask import Flask, request

app = Flask(__name__)

# Initialize global game state
board = [""] * 9
current_player = "X"
winner = None

def check_winner():
    global winner
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    for condition in win_conditions:
        a, b, c = condition
        if board[a] != "" and board[a] == board[b] == board[c]:
            winner = board[a]
            return True
    if "" not in board:
        winner = "Draw"
        return True
    return False

@app.route("/", methods=["GET", "POST"])
def game():
    global board, current_player, winner

    if request.method == "POST" and not winner:
        cell = int(request.form["cell"])
        if board[cell] == "":
            board[cell] = current_player
            if not check_winner():
                current_player = "O" if current_player == "X" else "X"

    board_html = ""
    for i in range(9):
        value = board[i]
        board_html += f'''
            <form method="POST" style="display:inline;">
                <input type="hidden" name="cell" value="{i}">
                <button type="submit" {'disabled' if value or winner else ''} style="width:80px;height:80px;font-size:30px;margin:5px;">
                    {value if value else ""}
                </button>
            </form>
        '''
        if i % 3 == 2:
            board_html += "<br>"

    result_html = ""
    if winner:
        result_html = f"<h2 style='color:green;'>Winner: {winner}</h2>" if winner != "Draw" else "<h2 style='color:orange;'>It's a Draw!</h2>"
        result_html += '''
            <form method="POST" action="/reset">
                <button type="submit" style="padding:10px 20px; font-size:16px;">Play Again</button>
            </form>
        '''

    return f"""
    <html>
    <head>
        <title>Tic Tac Toe</title>
    </head>
    <body style="text-align:center; font-family:Arial;">
        <h1>Tic Tac Toe</h1>
        <h3>Current Player: {current_player}</h3>
        {board_html}
        {result_html}
    </body>
    </html>
    """

@app.route("/reset", methods=["POST"])
def reset():
    global board, current_player, winner
    board = [""] * 9
    current_player = "X"
    winner = None
    return game()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

