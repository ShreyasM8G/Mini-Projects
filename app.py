from flask import Flask, render_template, request, redirect, url_for, jsonify, session, render_template_string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  
from flask import flash

app = Flask(__name__, static_url_path='/static')

app.secret_key = '' # Add a random secret key as you wish

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost/databse name'
db = SQLAlchemy(app)

class Player(db.Model):
    player_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mail_id = db.Column(db.String(255))
    dob = db.Column(db.String(50))
    age = db.Column(db.Integer)
    deposits = db.Column(db.Integer)
    mobile = db.Column(db.Integer)
    naame = db.Column(db.String(50))

class Developer(db.Model):
    dev_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dev_name = db.Column(db.String(40))
    mail_id = db.Column(db.String(100))
    mobile_no = db.Column(db.Integer)
    game_name = db.Column(db.String(200))

class Game(db.Model):
    game_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_name = db.Column(db.String(200))
    ppm = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(30))
    no_of_players = db.Column(db.Integer, nullable=False)
    dev_id = db.Column(db.Integer, db.ForeignKey('developer.dev_id'), nullable=False)

    developer = db.relationship('Developer', backref='games')

class Tournament(db.Model):
    tourn_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.game_id'))
    tourn_name = db.Column(db.String(100))
    game_name = db.Column(db.String(200))
    Entry_fee = db.Column(db.Integer, nullable=False)
    prize = db.Column(db.Integer, nullable=False)
    wint_id = db.Column(db.Integer, nullable=True)

    game = db.relationship('Game', backref='tournaments')

class Team(db.Model):
    team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tourn_id = db.Column(db.Integer, db.ForeignKey('tournament.tourn_id'))
    team_name = db.Column(db.String(200))
    game_name = db.Column(db.String(100))
    
    tournament = db.relationship('Tournament', backref='teams')

class TeamPlayer(db.Model):
    player_id = db.Column(db.Integer, db.ForeignKey('player.player_id'), primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), primary_key=True)
    
    player = db.relationship('Player', backref='teams')
    team = db.relationship('Team', backref='players')

class Matches(db.Model):
    match_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wint_id = db.Column(db.Integer, nullable=True)
    game_name = db.Column(db.String(200))
    team1_id = db.Column(db.Integer, db.ForeignKey('team.team_id'))
    team2_id = db.Column(db.Integer, db.ForeignKey('team.team_id'))
    tourn_id = db.Column(db.Integer, db.ForeignKey('tournament.tourn_id'))
    team1 = db.relationship('Team', foreign_keys=[team1_id])
    team2 = db.relationship('Team', foreign_keys=[team2_id])
    tournid = db.relationship('Tournament', foreign_keys=[tourn_id])

class Leaderboard(db.Model):
    player_id = db.Column(db.Integer, db.ForeignKey('player.player_id'), primary_key=True)
    points = db.Column(db.Integer, nullable=False)
    game_name = db.Column(db.String(200))
    player_name = db.Column(db.String(20))
    
    player = db.relationship('Player', backref='leaderboards')

class GamesPlayed(db.Model):
    player_id = db.Column(db.Integer, db.ForeignKey('player.player_id'), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.game_id'), primary_key=True)
    
    playerplayed = db.relationship('Player', backref='games')
    gameplayed = db.relationship('Game', backref='players')

# Routes
@app.route('/')
def home():
    return render_template('login.html')


@app.route('/mainpage')
def mainpage():
    username = session.get('username')
    return render_template('mainpage.html', username=username)


@app.route('/signup')
def signup():
    return render_template('sign_up.html')

@app.route('/admindex')
def admindex():
    return render_template('admindex.html')

@app.route('/admin_login')
def admin_login():
    return render_template('admin_log.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        
        user = Player.query.filter_by(naame=username, mail_id=email).first()

        if user:
            session['username'] = username
            session['player_id'] = user.player_id
            return redirect(url_for('mainpage'))
        else:
            error = 'Invalid username or email. Please try again.'
            return render_template('login.html', error=error)
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        username = request.form.get('username')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        age = request.form.get('Age')
        dob = request.form.get('dob')
        deposits = request.form.get('Points')

        new_player = Player(
            mail_id=email,
            dob=dob,
            age=age,
            deposits=deposits,
            mobile=mobile,
            naame=username
        )

        db.session.add(new_player)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('sign_up.html')

# Routes for Admin actions
@app.route('/create_match', methods=['POST'])
def create_match():
    if request.method == 'POST':
        team1_id = request.form.get('team1')
        team2_id = request.form.get('team2')
        tourn_id = request.form.get('tournament')
        game_name = request.form.get('game')

        new_match = Matches(
            team1_id=team1_id,
            team2_id=team2_id,
            game_name=game_name,
            tourn_id=tourn_id
        )

        db.session.add(new_match)
        db.session.commit()

        return jsonify({'message': 'Match created successfully'})
    
# Route for creating a tournament
@app.route('/create_tournament', methods=['POST'])
def create_tournament():
    if request.method == 'POST':
        tournament_name = request.form.get('tournament-name')
        game_id = request.form.get('game-id')
        game_name = request.form.get('tournament-game')
        prize_money = request.form.get('prize-money')
        participation_fee = request.form.get('participation-fee')

        new_tournament = Tournament(
            tourn_name=tournament_name,
            game_id=game_id,
            game_name=game_name,
            Entry_fee=participation_fee,
            prize=prize_money
        )

        db.session.add(new_tournament)
        db.session.commit()

        return jsonify({'message': 'Tournament created successfully'})
    
# Route for creating a team
@app.route('/create_team', methods=['POST'])
def create_team():
    if request.method == 'POST':
        tournament_id = request.form.get('tournament-id')
        game_name = request.form.get('team-game')
        team_name = request.form.get('team-name')
        player_ids = [int(player_id) for player_id in request.form.get('player-ids').split(',')]

        new_team = Team(
            tourn_id=tournament_id,
            game_name=game_name,
            team_name=team_name
        )

        db.session.add(new_team)
        db.session.commit()

        # Retrieve the team_id after committing the session
        team_id = new_team.team_id

        for player_id in player_ids:
            new_team_player = TeamPlayer(
                player_id=player_id,
                team_id=team_id
            )
            db.session.add(new_team_player)

        db.session.commit()

        return jsonify({'message': 'Team created successfully'})
    
# Route for creating a game
@app.route('/create_game', methods=['POST'])
def create_game():
    if request.method == 'POST':
        game_name = request.form.get('game-name')
        developer_id = request.form.get('developer-id')
        price = request.form.get('price')
        category = request.form.get('category')
        nop = request.form.get('nop')

        new_game = Game(
            game_name=game_name,
            ppm=price,
            no_of_players=nop,
            category=category,
            dev_id=developer_id
        )

        db.session.add(new_game)
       
        db.session.commit()

        return jsonify({'message': 'Game created successfully'})
    
# Route for adding a game developer
@app.route('/add_developer', methods=['POST'])
def add_developer():
    if request.method == 'POST':
        dev_name = request.form.get('developer-name')
        mobile_number = request.form.get('mobile-number')
        email_id = request.form.get('email-id')
        game_name = request.form.get('game-name')

        new_developer = Developer(
            dev_name=dev_name,
            mail_id=email_id,
            mobile_no=mobile_number,
            game_name=game_name
        )

        db.session.add(new_developer)
        db.session.commit()

        return jsonify({'message': 'Developer added successfully'})
    
# Route to get leaderboard data
@app.route('/get_leaderboard', methods=['GET'])
def get_leaderboard():
    app.logger.info("Fetching leaderboard data...")

    leaderboard_data = []
    leaderboard_data_query = text("SELECT player_id, points, game_name, player_name FROM leaderboard ORDER BY points DESC")
    
    result = db.session.execute(leaderboard_data_query)

    for row in result:
        # Use index-based access to retrieve values from the tuple
        entry = {'player_id': row[0], 'points': row[1], 'game_name': row[2], 'player_name': row[3]}
        leaderboard_data.append(entry)

    all_data = leaderboard_data

    # Create HTML table with column names
    table_html = '<thead><tr><th>Player ID</th><th>Score</th><th>Game</th><th>Player Name</th></tr></thead><tbody>'

    for row in all_data:
        # Adjust this part based on your data structure
        table_html += f'<tr><td>{row["player_id"]}</td><td>{row["points"]}</td><td>{row["game_name"]}</td><td>{row["player_name"]}</td></tr>'

    table_html += '</tbody>'

    return table_html


# Route for updating the leaderboard
@app.route('/update_leaderboard', methods=['POST'])
def update_leaderboard():
    if request.method == 'POST':
        player_id = request.form.get('player_id')
        points = request.form.get('points')
        game_name = request.form.get('game_name')
        player_name = request.form.get('player_name')

        # Check if the entry already exists in the leaderboard
        existing_entry = Leaderboard.query.filter_by(player_id=player_id).first()

        if existing_entry:
            # Update the existing entry
            existing_entry.points = points
            existing_entry.game_name = game_name
            existing_entry.player_name = player_name
        else:
            # Create a new entry in the leaderboard
            new_entry = Leaderboard(player_id=player_id, points=points, game_name=game_name, player_name=player_name)
            db.session.add(new_entry)

        # Commit changes to the database
        db.session.commit()

        return jsonify({'message': 'Leaderboard updated successfully'})

    return jsonify({'message': 'Invalid request'})


# Update the existing route for fetching developer data
@app.route('/get_developers', methods=['GET'])
def get_developers():
    app.logger.info("Fetching developer data...")

    developers_data = Developer.query.all()

    # Render the HTML table rows for developers
    rows = []
    for developer in developers_data:
        row = f'<tr><td>{developer.dev_id}</td><td>{developer.dev_name}</td><td>{developer.mail_id}</td><td>{developer.mobile_no}</td><td>{developer.game_name}</td></tr>'
        rows.append(row)

    return jsonify(rows)

@app.route('/get_matches', methods=['GET'])
def get_matches():
    app.logger.info("Fetching matches data...")

    matches_data = Matches.query.all()

    # Render the HTML table rows for matches
    rows = []
    for matches in matches_data:
        row = f'<tr><td>{matches.match_id}</td><td>{matches.wint_id}</td><td>{matches.game_name}</td><td>{matches.team1_id}</td><td>{matches.team2_id}</td><td>{matches.tourn_id}</td></tr>'
        rows.append(row)

    return jsonify(rows)


@app.route('/get_teams', methods=['GET'])
def get_teams():
    app.logger.info("Fetching teams data...")

    teams_data = Team.query.all()

    # Render the HTML table rows for teams
    rows = []
    for teams in teams_data:
        row = f'<tr><td>{teams.team_id}</td><td>{teams.tourn_id}</td><td>{teams.team_name}</td><td>{teams.game_name}</td></tr>'
        rows.append(row)

    return jsonify(rows)


@app.route('/get_teamplayers', methods=['GET'])
def get_teamplayers():
    app.logger.info("Fetching teamplayers data...")

    teamplayers_data = TeamPlayer.query.all()

    # Render the HTML table rows for teamplayers
    rows = []
    for teamplayer in teamplayers_data:
        row = f'<tr><td>{teamplayer.player_id}</td><td>{teamplayer.team_id}</td></tr>'
        rows.append(row)

    return jsonify(rows)


@app.route('/get_tournament', methods=['GET'])
def get_tournament():
    app.logger.info("Fetching tournaments data...")

    tournament_data = Tournament.query.all()

    # Render the HTML table rows for tournaments
    rows = []
    for tourn in tournament_data:
        row = f'<tr><td>{tourn.tourn_id}</td><td>{tourn.game_id}</td><td>{tourn.tourn_name}</td><td>{tourn.game_name}</td><td>{tourn.Entry_fee}</td><td>{tourn.wint_id}</td><td>{tourn.prize}</td></tr>'
        rows.append(row)

    return jsonify(rows)


@app.route('/get_players', methods=['GET'])
def get_players():
    app.logger.info("Fetching players data...")

    player_data = Player.query.all()

    # Render the HTML table rows for players
    rows = []
    for player in player_data:
        row = f'<tr><td>{player.player_id}</td><td>{player.mail_id}</td><td>{player.dob}</td><td>{player.age}</td><td>{player.deposits}</td><td>{player.mobile}</td><td>{player.naame}</td></tr>'
        rows.append(row)

    return jsonify(rows)

# Route for updating the leaderboard
@app.route('/update_matches', methods=['POST'])
def update_matches():
    if request.method == 'POST':
        match_id = request.form.get('match_id')
        wint_id = request.form.get('wint_id')

        # Check if the entry already exists in the leaderboard
        existing_entry = Matches.query.filter_by(match_id=match_id).first()

        if existing_entry:
            # Update the existing entry
            existing_entry.wint_id = wint_id
        else:
           pass

        # Commit changes to the database
        db.session.commit()

        return jsonify({'message': 'Leaderboard updated successfully'})

    return jsonify({'message': 'Invalid request'})


from flask import flash

@app.route('/update_tournament', methods=['POST'])
def update_tournament():
    try:
        # Get values from the form or request
        tournament_tourn_id = request.form.get('tourn_id')
        wint_id = request.form.get('twint_id')

        # Check if wint_id is not empty before updating
        if wint_id and wint_id.isdigit():
            # Convert wint_id to integer before updating
            wint_id = int(wint_id)

            # Perform the update
            tournament = Tournament.query.get(tournament_tourn_id)
            tournament.wint_id = wint_id
            db.session.commit()

            flash('Tournament updated successfully', 'success')
        else:
            # Handle the case where wint_id is empty or not a valid integer
            flash('Invalid value for wint_id', 'error')

    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')

    return redirect('/mainpage')



# Route for updating the leaderboard
@app.route('/update_player', methods=['POST'])
def update_player():
    if request.method == 'POST':
        player_id = request.form.get('player_id')
        deposits = request.form.get('deposits')

        # Check if the entry already exists in the leaderboard
        existing_entry = Player.query.filter_by(player_id=player_id).first()

        if existing_entry:
            # Update the existing entry
            existing_entry.deposits = int(existing_entry.deposits) + int(deposits)

        else:
           pass

        # Commit changes to the database
        db.session.commit()

        return jsonify({'message': 'Player updated successfully'})

    return jsonify({'message': 'Invalid request'})


@app.route('/gamepage')
def gamepage():
    player_id = session.get('player_id')
    return render_template('games.html', player_id=player_id)


# Add this route to handle adding games to the GamesPlayed table
@app.route('/addgames_played', methods=['POST'])
def addgames_played():
    if request.method == 'POST':
        player_id = request.form.get('player_id')
        game_id = request.form.get('game_id')

        # Create a new entry in the GamesPlayed table
        new_entry = GamesPlayed(player_id=int(player_id), game_id=int(game_id))
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({'message': 'Game played entry added successfully'})

    return jsonify({'message': 'Invalid request'})


@app.route('/tt_update', methods=['POST', 'GET'])
def tt_update():
    global teams_data  

    if request.method == 'POST':
    
            # Get the tournament ID from the form data
            tt_id = request.form.get('ttid')

            # Use SQLAlchemy to execute the SQL query
            teams_data = Team.query.filter_by(tourn_id=tt_id).all()

            rows = []
            for team in teams_data:
                row = f'<tr><td>{team.team_id}</td><td>{team.team_name}</td></tr>'
                rows.append(row)

            return jsonify(rows)

    return jsonify({'message': 'Invalid request'})


@app.route('/tm_update', methods=['POST', 'GET'])
def tm_update():
    global matches_data

    if request.method == 'POST':
        # Get the tournament ID from the form data
        tm_id = request.form.get('tmid')

        # Use the 'text' function to declare the SQL expression
        match_details_query = text("CALL GetMatchDetailsByTournament(:tm_id)")

        # Execute the SQL expression with parameters
        matchs_data = db.session.execute(match_details_query, {'tm_id': tm_id})

        rows = []
        for match in matchs_data:
            row = f'<tr><td>{match.match_id}</td><td>{match.game_name}</td><td>{match.team1_id}</td><td>{match.team1_name}</td><td>{match.team2_id}</td><td>{match.team2_name}</td></tr>'
            rows.append(row)

        return jsonify(rows)

    return jsonify({'message': 'Invalid request'})


@app.route('/tg_update', methods=['POST', 'GET'])
def tg_update():

    if request.method == 'POST':
        # Get the game_id from the query parameters
        tg_id = request.form.get('tgid')

        # Check if tg_id is not None before converting to an integer
        if tg_id is not None:
            tg_id = int(tg_id)

            # Query the tournaments for the given game_id
            tournaments_data = Tournament.query.filter_by(game_id=tg_id).all()

            rows = []
            for tg in tournaments_data:
                row = f'<tr><td>{tg.tourn_id}</td><td>{tg.tourn_name}</td><td>{tg.tourn_id}</td><td>{tg.tourn_id}</td></tr>'
                rows.append(row)

            return jsonify(rows)
        
    return jsonify({'message': 'Invalid request'})
    
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
