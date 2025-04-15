from flask import Flask, render_template, request, redirect, url_for
from models import db, Team, Player, Match
import pandas as pd


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sports.db'
db.init_app(app)

@app.route('/')
def home():
    matches = Match.query.all()
    teams = Team.query.all()
    return render_template('index.html', matches=matches, teams=teams)
@app.route('/add_match', methods=['POST'])
def add_match():
    team1 = Team.query.get(request.form['team1'])
    team2 = Team.query.get(request.form['team2'])
    new_match = Match(team1_id=team1.id, team2_id=team2.id, date=request.form['date'])
    db.session.add(new_match)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/update_score/<int:match_id>', methods=['POST'])
def update_score(match_id):
    match = Match.query.get(match_id)
    match.team1_score = request.form['team1_score']
    match.team2_score = request.form['team2_score']
    match.status = "Completed"
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/standings')
def standings():
    teams = Team.query.all()
    standings_data = []
    for team in teams:
        wins = Match.query.filter(
            ((Match.team1_id == team.id) & (Match.team1_score > Match.team2_score)) |
            ((Match.team2_id == team.id) & (Match.team2_score > Match.team1_score))
        ).count()
        standings_data.append({"Team": team.name, "Wins": wins})
    
    df = pd.DataFrame(standings_data).sort_values("Wins", ascending=False)
    return render_template('standings.html', tables=[df.to_html(classes='data')])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)