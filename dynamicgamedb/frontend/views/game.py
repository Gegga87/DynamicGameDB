from dynamicgamedb.frontend import frontend, dgdb
from flask import request, jsonify, redirect, url_for, render_template
from dynamicgamedb.frontend.api_com import DynamicGameDB, Game
import sys, traceback

@frontend.route('/games', methods=['GET', 'POST'])
def games():
    print "games"
    games = dgdb.games()
    print "games return"
          # should be changed to what the search query was for
    if request.method == 'POST':
        search=request.form['search_field']
        return render_template("games.html", games=games, search=search)
    else: 
    # games_list = []
    # for game in games:
    #     games_list = games_list + " - %d %s %s %s" % (game.id, game.title, game.platform, game.developer)
        search = "GET"
        return render_template("games.html", games=games, search=search)
    

    #return render_template("games.html", games=games)

@frontend.route('/game/<int:id>', methods=['GET'])
def game(id):
    game = dgdb.game(id)
    games = dgdb.games()
    #game_str = "%d %s %s %s" % (game.id, game.title, game.platform, game.developer)
    return render_template("game.html", game=game, games=games)

@frontend.route('/game/add', methods=['GET','POST'])
def add_game():
    game = dgdb.add_game(title="Ett nytt spel", platform_id=2)
    platforms=["SNES","NES","PC"]
   
    print "Gameid: ", game.id
    if request.method == 'POST':
        title = request.form['title']
        platform = request.form['platform']
        print "title:", title
        print "platform:", platform
        return render_template('add_game.html', platforms=platforms)
    else:
        #TODO: form page for Adding games
        return render_template('add_game.html', platforms=platforms)

@frontend.route('/game/<int:id>/edit', methods=['GET','POST'])
def edit_game(id):
    print "edit game"
    #TODO: extended form page for editing games and givinhg additional data
    return "edit game"

@frontend.route('/game/<int:id>/connection', methods=['POST'])
def connect_game():
    print "Connecting Games :D"
    #TODO: connection mechanics
    return "connect game"