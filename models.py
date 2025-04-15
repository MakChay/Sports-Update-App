from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    
    # Relationships
    home_matches = db.relationship('Match', foreign_keys='Match.team1_id', backref='home_team', lazy=True)
    away_matches = db.relationship('Match', foreign_keys='Match.team2_id', backref='away_team', lazy=True)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    goals = db.Column(db.Integer, default=0)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team1_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team2_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    team1_score = db.Column(db.Integer, default=0)
    team2_score = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default="Upcoming")

def create_default_teams(app):
    with app.app_context():
        default_teams = ["Lions", "Tigers", "Eagles", "Bears", "Wolves"]
        for team_name in default_teams:
            if not Team.query.filter_by(name=team_name).first():
                team = Team(name=team_name)
                db.session.add(team)
        db.session.commit()