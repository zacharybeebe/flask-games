from flask import Flask, redirect, render_template, request, url_for, jsonify, make_response
from flask_socketio import SocketIO, send
from utils import *

app = Flask(__name__)
app.config['SECRET_KEY'] = """6@|J~j388*5{ijgKh33+{4}6{-Hw%d7#"""
app.config['GAME'] = get_new_game()

app_socket = SocketIO(app)

# Use this bool to control your app debug state, run.py will import this
DEBUG = True
if DEBUG:
    # debug server settings
    HOST = '127.0.0.1'
    PORT = 5000
else:
    # local network settings
    HOST = '146.76.96.39'
    PORT = 8080

SOCKET_LOC = f'http://{HOST}:{PORT}'


# Flask-SocketIO handling messages
@app_socket.on('message')
def handle_message(message):
    send(message, broadcast=True)


# Resets the game for the current user
@app.route('/reset')
def reset():
    app.config['GAME'] = get_new_game()
    send('reset@null?null?null?@none', broadcast=True, namespace='/')
    return redirect(url_for('index'))


# Resets the game for the other user
@app.route('/client_reset')
def client_reset():
    return redirect(url_for('index'))


# Starts a new game, players wil select which player they are
@app.route('/', methods=['POST', 'GET'])
def index():
    game = app.config['GAME']
    current_player = None

    if request.method == 'POST':
        for key, val in request.form.items():
            if val == '1':
                current_player = key
                game[current_player]['in'] = True
                break
        send('reload@null?null?null?@none', broadcast=True, namespace='/')
        return redirect(url_for('game', player=current_player))

    return render_template('index.html', game=game, player=current_player, loc=SOCKET_LOC)


# Main game play - battleship shot selection is done asynchronously, received and sent by hit_select
@app.route('/game_<player>', methods=['POST', 'GET'])
def game(player):
    game = app.config['GAME']
    pgame = game[player]

    if player == 'player1':
        othergame = game['player2']
    else:
        othergame = game['player1']

    if request.method == 'POST':
        if not pgame['ready']:
            pgame['ready'] = True
            for key, value in request.form.items():
                if key.startswith('i?'):
                    letter, number, boat = key.split('?')[-1].split('|')
                    number = int(number)
                    pgame['board'][letter][number]['fill'] = value
                    if boat != 'none':
                        pgame['boats'][boat][f'{letter}{number}'] = False

                        pgame['board'][letter][number]['id'] = f'{letter}|{number}|{boat}'
                        othergame['attack'][letter][number]['id'] = f'{letter}|{number}|{boat}'

            if othergame['ready']:
                send(f'ready@null?null?null?@{player.upper()}', broadcast=True, namespace='/')

    return render_template('game.html', player=player, gameover=game['gameover'], pgame=pgame, othergame=othergame, boats=BOATS)


@app.route('/hit_select', methods=['POST'])
def hit_select():
    post = request.get_json()
    player = post['player']
    cell = post['cell']

    game = app.config['GAME']
    if player == 'player1':
        pgame = game['player1']
        othergame = game['player2']
    else:
        pgame = game['player2']
        othergame = game['player1']

    pgame['turn'] = False
    othergame['turn'] = True

    othergame['attacks'].append(cell)

    letter, number, boat = cell.split('|')
    number = int(number)

    win = False
    boat_sunk = None
    hit = False

    if othergame['board'][letter][number]['fill'] == 'fill':
        hit = True
        othergame['board'][letter][number]['is_hit'] = 'is_hit'
        othergame['boats'][boat][f'{letter}{number}'] = True
        pgame['attack'][letter][number]['has_hit'] = 'has_hit'

        if all([value for value in othergame['boats'][boat].values()]):
            boat_sunk = boat.upper()
            othergame['sunk'].append(boat)
            print(f'{boat_sunk=}')
            all_boats = 1
            for boat_check in othergame['boats']:
                if boat_check != boat:
                    if all([value for value in othergame['boats'][boat_check].values()]):
                        all_boats += 1
            if all_boats == 5:
                win = True
                for p_boat in pgame['boats']:
                    for key in pgame['boats'][p_boat]:
                        letter = key[0]
                        number = int(key[1:])
                        if p_boat not in pgame['sunk']:
                            othergame['attack'][letter][number]['fill'] = 'remain'
                        else:
                            othergame['attack'][letter][number]['fill'] = 'show'

    else:
        othergame['board'][letter][number]['is_miss'] = 'is_miss'
        pgame['attack'][letter][number]['has_miss'] = 'has_miss'

    if win:
        pmsg = f"{letter}{number} is a HIT!!\n\nYOU HAVE SUNK THE OTHER PLAYER'S {boat_sunk}!\n\nYOU HAVE SUNKEN ALL THE BOATS, YOU WIN!!!"
        omsg = f"{letter}{number} is a HIT!!\n\nYOUR {boat_sunk} HAS BEEN SUNK\n\nALL YOUR BOATS HAVE SEEN SUNK, YOU LOSE!!"
        game['gameover'] = True
    elif boat_sunk is not None:
        pmsg = f"{letter}{number} is a HIT!!\n\nYOU HAVE SUNK THE OTHER PLAYER'S {boat_sunk}!"
        omsg = f"{letter}{number} is a HIT!!\n\nYOUR {boat_sunk} HAS BEEN SUNK"
    elif hit:
        pmsg = f"{letter}{number} is a HIT!!"
        omsg = f"{letter}{number} is a HIT!!"
    else:
        pmsg = f"{letter}{number} is a MISS.."
        omsg = f"{letter}{number} is a MISS.."

    send(f'update@{omsg}@{player}', broadcast=True, namespace='/')
    return make_response(jsonify({'win': win, 'message': pmsg}), 200)


if __name__ == '__main__':
    app_socket.run(app, host=HOST, port=PORT, debug=DEBUG)
