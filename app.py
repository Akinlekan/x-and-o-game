from flask import Flask, render_template, request, jsonify, session
import json

app = Flask(__name__)
app.secret_key = 'tic_tac_toe_secret_key_2024'

def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    for combo in winning_combinations:
        if board[combo[0]] and board[combo[0]] == board[combo[1]] == board[combo[2]]:
            return board[combo[0]], combo
    return None, None

def is_draw(board):
    return all(cell != '' for cell in board) 

def get_ai_move(board):
    def minimax(board, is_maximizing):
        winner, _ = check_winner(board)
        if winner == 'O':
            return 10
        if winner == 'X':
            return -10
        if is_draw(board):
            return 0

        if is_maximizing:
            best = -1000
            for i in range(9):
                if board[i] == '':
                    board[i] = 'O'
                    best = max(best, minimax(board, False))
                    board[i] = ''
            return best
        else:
            best = 1000
            for i in range(9):
                if board[i] == '':
                    board[i] = 'X'
                    best = min(best, minimax(board, True))
                    board[i] = ''
            return best

    best_val = -1000
    best_move = -1
    for i in range(9):
        if board[i] == '':
            board[i] = 'O'
            move_val = minimax(board, False)
            board[i] = ''
            if move_val > best_val:
                best_val = move_val
                best_move = i
    return best_move

@app.route('/')
def index():
    session['board'] = [''] * 9
    session['current_player'] = 'X'
    session['game_over'] = False
    session['scores'] = session.get('scores', {'X': 0, 'O': 0, 'Draw': 0})
    return render_template('index.html', scores=session['scores'])

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    cell = data.get('cell')
    mode = data.get('mode', 'pvp')

    board = session.get('board', [''] * 9)
    current_player = session.get('current_player', 'X')
    game_over = session.get('game_over', False)
    scores = session.get('scores', {'X': 0, 'O': 0, 'Draw': 0})

    if game_over or board[cell] != '':
        return jsonify({'error': 'Invalid move'}), 400

    board[cell] = current_player
    winner, winning_combo = check_winner(board)

    if winner:
        scores[winner] = scores.get(winner, 0) + 1
        session['scores'] = scores
        session['board'] = board
        session['game_over'] = True
        return jsonify({
            'board': board,
            'winner': winner,
            'winning_combo': winning_combo,
            'scores': scores,
            'game_over': True
        })

    if is_draw(board):
        scores['Draw'] = scores.get('Draw', 0) + 1
        session['scores'] = scores
        session['board'] = board
        session['game_over'] = True
        return jsonify({
            'board': board,
            'draw': True,
            'scores': scores,
            'game_over': True
        })

    next_player = 'O' if current_player == 'X' else 'X'
    ai_move = None

    if mode == 'pvc' and next_player == 'O':
        ai_move = get_ai_move(board)
        board[ai_move] = 'O'
        winner, winning_combo = check_winner(board)

        if winner:
            scores[winner] = scores.get(winner, 0) + 1
            session['scores'] = scores
            session['board'] = board
            session['game_over'] = True
            return jsonify({
                'board': board,
                'winner': winner,
                'winning_combo': winning_combo,
                'scores': scores,
                'game_over': True,
                'ai_move': ai_move
            })

        if is_draw(board):
            scores['Draw'] = scores.get('Draw', 0) + 1
            session['scores'] = scores
            session['board'] = board
            session['game_over'] = True
            return jsonify({
                'board': board,
                'draw': True,
                'scores': scores,
                'game_over': True,
                'ai_move': ai_move
            })

        session['board'] = board
        session['current_player'] = 'X'
        return jsonify({
            'board': board,
            'current_player': 'X',
            'ai_move': ai_move,
            'game_over': False
        })

    session['board'] = board
    session['current_player'] = next_player
    return jsonify({
        'board': board,
        'current_player': next_player,
        'game_over': False
    })

@app.route('/reset', methods=['POST'])
def reset():
    scores = session.get('scores', {'X': 0, 'O': 0, 'Draw': 0})
    session['board'] = [''] * 9
    session['current_player'] = 'X'
    session['game_over'] = False
    return jsonify({'board': [''] * 9, 'current_player': 'X', 'scores': scores})

@app.route('/reset_scores', methods=['POST'])
def reset_scores():
    session['scores'] = {'X': 0, 'O': 0, 'Draw': 0}
    session['board'] = [''] * 9
    session['current_player'] = 'X'
    session['game_over'] = False
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
