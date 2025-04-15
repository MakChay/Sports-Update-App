from app import app, db
import os

with app.app_context():
    # This will delete AND recreate the database
    db.drop_all()
    db.create_all()
    print("Database completely reset!")