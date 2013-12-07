# -*- coding: utf-8 -*-
from dynamicgamedb.backend import backend, oid
from dynamicgamedb.backend.model import Game, Platform, User, Relation
from dynamicgamedb.backend.database import db_session
from flask import Response, request, jsonify, redirect, url_for, session
import dateutil.parser
FRONTEND_URL = 'http://localhost:8000'

@backend.route('/api/logout/')
def logout():
    session.pop('openid', None)
    #flash(u'You were signed out')
    return redirect(oid.get_next_url())

@backend.route('/api/login/')
@oid.loginhandler
def api_login():
    client_id = request.args.get("client_id", None)
    print "clientid: ", client_id
    if not client_id:
        """
        response = Response(    ## This should totaly be defined as a helper function somewhere...
            json.dumps({"error": { 
                "type": "DGDBApiException", 
                "message": "Why did you forget client_id!?" 
            }}),
            mimetype="application/json",
            status=400 # Bad request, bad!
        )
        return response
        """
        print "Something went wrong but I'll allow it for now"
        ##return "This is wrong"
    session['client_id'] = client_id
    ## Get client from some magical database of accepted clients
    # client = magic
    # if client:
    if not "openid" in session:
        print "not openid"
        # Redirect to google 
        # But for now redirect to a fake endpoint
        print "redirect to google"
        return oid.try_login( 'https://www.google.com/accounts/o8/id', ask_for=['email'])
    else:
        print "openid in session: ", session['openid']
        # Already logged in but didn't know it so we provide a new code for them
        # to generate a new token.
        # Store one time token in database
        # Redirect to frontend with a code so that frontend can request a new token
        return redirect(FRONTEND_URL+'/auth/?one_time_token=1337')

@oid.after_login
def create_or_login(resp):
    print "create or login"
    session['openid'] = resp.identity_url
    user = db_session.query(User).filter_by(openid=resp.identity_url).first()
    if user is not None:
        #flash(u'Successfully signed in')
        print "user found - openid: ", session['openid']
        g.user = user
        return redirect(FRONTEND_URL+'/auth/?one_time_token=1337')
    print "no user - openid: ", session['openid']
    db_session.add(User(openid=session['openid'], email=resp.email))
    db_session.commit()
    return redirect(FRONTEND_URL+'/auth/?one_time_token=1337')

@backend.route('/api/token', methods=['GET','POST'])
@backend.route('/api/token/', methods=['GET','POST'])
def api_token():
    print "api token"
    ott = request.form.get('one_time_token', None)
    #ott = request.args.get("one_time_token", None)
    if not ott:
        return "there is no one time token biatch"
    # Get one time token from database 
    # check if it existed as described in database
    token = 7331 #Generate magical token and store in database
    print "returning token 7331"
    return str(token)

@backend.route('/api/user/')
def user():
    token = request.args.get("user_token", None)
    if not token:
        return "lol failure"
    
    #Get openid from token
    user = db_session.query(User).get(token)
    return jsonify({"user_email":user.email})

@backend.route('/initp', methods=['GET'])
def initp():
    p1 = Platform("PC")
    db_session.add(p1)
    p2 = Platform("Xbox 360")
    db_session.add(p2)
    p3 = Platform("PlayStation 3")
    db_session.add(p3)
    p4 = Platform("PlayStation 4")
    db_session.add(p4)
    p5 = Platform("Xbox One")
    db_session.add(p5)
    p6 = Platform("Nintendo Entertainment System")
    db_session.add(p6)
    db_session.commit()
    return redirect(url_for('backend.platforms'))

@backend.route('/initg', methods=['GET'])
def initg():
    platform = db_session.query(Platform).get(1)
    game1 = Game("Kattspelet",platform)
    game2 = Game("Hundspelet",platform)
    game3 = Game("Battlefield 3",platform)
    game4 = Game("Ett spel om fiskar",platform)
    #nintendo = db_session.query(Platform).get(6)
    #print nintendo.name
    #game5 = Game("Tetris",nintendo)
    #game6 = Game("Ett irriterande långt spelnamn kanske", nintendo) #Fungerar ej Yay! För långt eller pga åäö?
    #game7 = Game("Ölspelet", nintendo)
    db_session.add(game1)
    db_session.add(game2)
    db_session.add(game3)
    db_session.add(game4)
    #db_session.add(game5)
    #db_session.add(game6)
    #db_session.add(game7)
    db_session.commit()
    return redirect(url_for('backend.games'))


@backend.route("/init_server")
def init_server():
    #**********platforms************
    p1 = Platform("PC")
    db_session.add(p1)
    p2 = Platform("Xbox 360")
    db_session.add(p2)
    p3 = Platform("PlayStation 3")
    db_session.add(p3)
    p4 = Platform("PlayStation 4")
    db_session.add(p4)
    p5 = Platform("Xbox One")
    db_session.add(p5)
    p6 = Platform("Nintendo Entertainment System")
    db_session.add(p6)
    db_session.commit()
    #**********games************
    game1 = Game("Battlefield 3",p1)
    game1.developer = "DICE"
    game1.info = "Battlefield 3 is a First-Person Shooter (FPS) that is designed to attack your senses, delivering a visceral combat experience like no other FPS before it. Sequel to 2005's Battlefield 2, Battlefield 3 utilizes the updated Frostbite 2 game engine, which allows for advanced destruction, sound, and graphics as well as a focus on dense in-game urban settings."
    game1.picture = "http://upload.wikimedia.org/wikipedia/en/6/69/Battlefield_3_Game_Cover.jpg"
    game1.publisher = "EA"
    game1.release_date =  dateutil.parser.parse("2011-10-25")
    game1.relations = 3
    db_session.add(game1)

    game2 = Game("ARMA 3",p1)
    game2.developer = "Bohemia Interactive"
    game2.info = "After years of intense warfare against Eastern armies, Europe has become the last stand for the battered NATO forces. On the verge of being driven into the sea, NATO command embarks upon a most desperate measure. In the hope of seizing what seems to be a well-guarded military secret, Operation Magnitude is launched. A small group of Special Forces and Researchers are sent to a Mediterranean island deep behind enemy lines."
    game2.picture = "http://www.blogcdn.com/www.joystiq.com/media/2013/03/arma-3-cover.jpg"
    game2.publisher = "Bohemia Interactive"
    game2.release_date =  dateutil.parser.parse("2013-09-12")
    game2.relations = 2
    db_session.add(game2)

    game3 = Game("Grand Theft Auto: Vice City",p1)
    game3.developer = "Rockstar North"
    game3.info = "SOMETEXT"
    game3.picture = "http://upload.wikimedia.org/wikipedia/en/c/ce/Vice-city-cover.jpg"
    game3.publisher = "Rockstar"
    game3.release_date =  dateutil.parser.parse("2002-10-27")
    game3.relations = 2
    db_session.add(game3)

    game4 = Game("Battlefield 4",p1)
    game4.developer = "DICE"
    game4.info = "Battlefield 4 is the genre-defining action blockbuster made from moments that blur the line between game and glory. Fueled by the next-generation power and fidelity of Frostbite 3, Battlefield 4 provides a visceral, dramatic experience unlike any other."
    game4.picture = "http://upload.wikimedia.org/wikipedia/en/e/ed/Battlefield_4.jpg"
    game4.publisher = "EA"
    game4.release_date =  dateutil.parser.parse("2013-10-29")
    game4.relations = 2
    db_session.add(game4)

    game5 = Game("Minecraft",p1)
    game5.developer = "Mojang"
    game5.info = "Minecraft is a sandbox indie game originally created by Swedish programmer Markus \"Notch\" Persson and later developed and published by Mojang. It was publicly released for the PC on May 17, 2009, as a developmental alpha version and, after gradual updates, was published as a full release version on November 18, 2011."
    game5.picture = "http://pcgamerparadise.com/images/Minecraft_cover.jpg"
    game5.publisher = "Mojang"
    game5.release_date =  dateutil.parser.parse("2009-05-17")
    game5.relations = 2
    db_session.add(game5)

    game6 = Game("Terraria",p1)
    game6.developer = "Re-Logic"
    game6.info = "Terraria is an open-ended sandbox 2D game with gameplay revolved around exploration, building, and action. The game has a 2D sprite tile-based graphical style reminiscent of the 16-bit sprites found on the SNES. The game is noted for its classic exploration-adventure style of play, similar to titles such as Metroid and Minecraft."
    game6.picture = "http://www.pageofreviews.com/wp-content/uploads/terraria1.png"
    game6.publisher = "Re-Logic"
    game6.release_date =  dateutil.parser.parse("2011-05-16")
    game6.relations = 1
    db_session.add(game6)

    game7 = Game("Ace of Spades",p1)
    game7.developer = "Jagex Game Studio"
    game7.info = "Ace of Spades is a sandbox building and FPS game, originally developed by Ben Aksoy for the PC and released in 2011 as a beta version. In late 2012, RuneScape developer, Jagex took over development of the game, making it payware on Steam and updating its gameplay."
    game7.picture = "http://media.ign.com/games/image/object/106/106949/Ace-Of-Spades_PCDL.jpg"
    game7.publisher = "Jagex Game Studio"
    game7.release_date =  dateutil.parser.parse("2012-12-12")
    game7.relations = 2
    db_session.add(game7)

    game8 = Game("Fallout 2",p1)
    game8.developer = ""
    game8.info = ""
    game8.picture = "http://pics.mobygames.com/images/covers/large/1124464345-00.jpg"
    game8.publisher = ""
    game8.release_date =  dateutil.parser.parse("2013-12-29")
    db_session.add(game8)

    game9 = Game("Dishonored",p1)
    game9.developer = "Arkane Studios"
    game9.info = ""
    game9.picture = "http://i.imgur.com/CMiXt.jpg"
    game9.publisher = "Bethesda Softworks"
    game9.release_date =  dateutil.parser.parse("2012-10-09")
    game9.relations = 1
    db_session.add(game9)

    game10 = Game("Saints Row IV",p1)
    game10.developer = "Volition Inc"
    game10.info = ""
    game10.picture = "http://fronttowardsgamer.com/wp-content/uploads/2013/05/srivbox.jpg"
    game10.publisher = "Deep Silver"
    game10.release_date =  dateutil.parser.parse("2013-08-20")
    game10.relations = 1
    db_session.add(game10)

    game11 = Game("Prototype 2",p1)
    game11.developer = "Radical Entertainment"
    game11.info = "SOMETEXT"
    game11.picture = "http://www.yellmagazine.com/wp-content/uploads/2012/05/prototype-2-cover.jpg"
    game11.publisher = "Activision"
    game11.release_date =  dateutil.parser.parse("2012-04-24")
    game11.relations = 2
    db_session.add(game11)


    #***********relation*********************
    rel = Relation(game1, game2)    #BF3 -> ARMA 3
    db_session.add(rel)
    rel = Relation(game1, game4)    #BF3 -> BF4
    db_session.add(rel)
    rel = Relation(game2, game4)    #BF4 -> ARMA 3
    db_session.add(rel)
    rel = Relation(game1, game7)    #BF3 -> Ace of spades
    db_session.add(rel)
    rel = Relation(game5, game7)    #Minecraft -> Ace of spades
    db_session.add(rel)
    rel = Relation(game5, game6)    #Minecraft -> Terraria
    db_session.add(rel)
    rel = Relation(game3, game11)    #GTA:Vice city -> prototype 2
    db_session.add(rel)
    rel = Relation(game3, game10)    #GTA:Vice city -> Saints row
    db_session.add(rel)
    rel = Relation(game11, game9)    #prototype 2 -> Dishonored
    db_session.add(rel)

    db_session.commit()
    return redirect(url_for('backend.games'))