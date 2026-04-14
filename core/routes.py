from flask import render_template, url_for, request, make_response, jsonify, redirect
from core import app
from core.leaderboard import Leaderboard

@app.route('/')
def index():
    return render_template('index.html',)

@app.route('/contato')
def contato():
    return render_template('contato.html',)

@app.route('/placar')
def placar():
    return render_template('placar.html', entries=Leaderboard)

@app.route('/placar/add', methods=['GET'])
def placar_add():
    match = {
          "nickname": "paulo",
          "score": "99988",
          "seconds": "120",
          "text": "",
          "date": "4/14/2025 19:06:51"
        }
    leaderboard = Leaderboard
    leaderboard.append(match)
    return redirect(url_for('placar'))

@app.route('/placar/rm', methods=['GET'])
def placar_rm():
    leaderboard = Leaderboard
    leaderboard.pop()
    return redirect(url_for('placar'))

@app.route('/leaderboard')
def leaderboard():
    return make_response(
        jsonify(Leaderboard)
    )

