from flask import Flask, render_template, request, redirect, url_for
from models import db, Team, Player, Match, create_default_teams

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sports.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    matches = Match.query.all()
    teams = Team.query.all()
    return render_template('index.html', matches=matches, teams=teams)

@app.route('/add_match', methods=['POST'])
def add_match():
    team1_id = request.form['team1']
    team2_id = request.form['team2']
    date = request.form['date']
    
    new_match = Match(
        team1_id=team1_id,
        team2_id=team2_id,
        date=date,
        status="Upcoming"
    )
    db.session.add(new_match)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/update_score', methods=['POST'])
def update_score():
    match_id = request.form['match_id']
    match = Match.query.get(match_id)
    
    match.team1_score = request.form['team1_score']
    match.team2_score = request.form['team2_score']
    match.status = "Completed"
    
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_teams(app)
    app.run(debug=True)