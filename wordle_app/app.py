from flask import Flask, redirect, render_template, request, url_for
from flask_socketio import SocketIO, send
from utils import *

app = Flask(__name__)
app.config['SECRET_KEY'] = """6@|J~j388*5{ijgKh33+{4}6{-Hw%d7#"""
app.config['GAME'] = get_new_game()

app_socket = SocketIO(app)

# Use this bool to control your app debug state, run.py will import this
DEBUG = False
if DEBUG:
    # Debug server
    HOST = '127.0.0.1'
    PORT = 5000
else:
    # Local network serve
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
    send('reset!null?null?null?', broadcast=True, namespace='/')
    return redirect(url_for('index'))


# Resets the game for the other user
@app.route('/client_reset')
def client_reset():
    return redirect(url_for('index'))


# Main game play
@app.route('/', methods=['POST', 'GET'])
def index():
    game = app.config['GAME']

    if request.method == 'POST':
        word = game['word']
        guess = ''.join(list(request.form.values())).upper()

        if guess not in game['word_guesses']:
            game['word_guesses'].append(guess)
            current_row = int(list(request.form.keys())[0][0])

            # Algorithm for determining how to mark characters ##############################################
            corrects = {i: guess[i] for i in range(len(guess)) if word[i] == guess[i]}
            word_counts = {ch: game['word_list'].count(ch) for ch in game['word_list']}
            for ch in corrects.values():
                word_counts[ch] -= 1

            guess_row_list = []
            for i, ch in enumerate(guess):
                if game['word_idx'][i] == ch:
                    color = 'green'

                elif ch in word:
                    if word_counts[ch] > 0:
                        word_counts[ch] -= 1
                        color = 'blue'
                    else:
                        color = 'none'
                else:
                    color = 'none'
                    game['missed_letters'].append(ch)
                guess_row_list.append([ch, color])
            ###################################################################################################

            game['guesses'][current_row] = guess_row_list

            game['missed_letters'] = list(set(game['missed_letters']))
            game['row'] += 1

            if guess == word:
                game['correct'] = True

            elif game['row'] == 6:
                game['gameover'] = True

            send('reload!null?null?null?', broadcast=True, namespace='/')

    return render_template('index.html', word=game['word'], row=game['row'], guesses=game['guesses'], correct=game['correct'], gameover=game['gameover'],
                           regex=get_regex(game['missed_letters']), loc=SOCKET_LOC)


if __name__ == '__main__':
    app_socket.run(app, host=HOST, port=PORT, debug=DEBUG)
