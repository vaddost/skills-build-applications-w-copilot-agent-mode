from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        from pymongo import MongoClient
        from datetime import date
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        # Видалення всіх колекцій octofit_tracker_*
        for name in db.list_collection_names():
            if name.startswith('octofit_tracker_'):
                db.drop_collection(name)

        # Teams
        marvel_id = db['octofit_tracker_team'].insert_one({"name": "Marvel", "description": ""}).inserted_id
        dc_id = db['octofit_tracker_team'].insert_one({"name": "DC", "description": ""}).inserted_id

        # Users
        tony_id = db['octofit_tracker_user'].insert_one({"email": "tony@stark.com", "name": "Tony Stark", "team": "Marvel", "is_superhero": True}).inserted_id
        steve_id = db['octofit_tracker_user'].insert_one({"email": "steve@rogers.com", "name": "Steve Rogers", "team": "Marvel", "is_superhero": True}).inserted_id
        bruce_id = db['octofit_tracker_user'].insert_one({"email": "bruce@wayne.com", "name": "Bruce Wayne", "team": "DC", "is_superhero": True}).inserted_id
        clark_id = db['octofit_tracker_user'].insert_one({"email": "clark@kent.com", "name": "Clark Kent", "team": "DC", "is_superhero": True}).inserted_id

        # Activities
        today = date.today().isoformat()
        db['octofit_tracker_activity'].insert_many([
            {"user_id": tony_id, "type": "run", "duration": 30, "date": today},
            {"user_id": steve_id, "type": "cycle", "duration": 60, "date": today},
            {"user_id": bruce_id, "type": "swim", "duration": 45, "date": today},
            {"user_id": clark_id, "type": "run", "duration": 50, "date": today},
        ])

        # Workouts
        db['octofit_tracker_workout'].insert_many([
            {"name": "Super Strength", "description": "Power workout", "suggested_for": "dc"},
            {"name": "Agility Boost", "description": "Speed and agility", "suggested_for": "marvel"},
        ])

        # Leaderboard
        db['octofit_tracker_leaderboard'].insert_many([
            {"user_id": tony_id, "score": 100, "rank": 2},
            {"user_id": steve_id, "score": 90, "rank": 4},
            {"user_id": bruce_id, "score": 95, "rank": 3},
            {"user_id": clark_id, "score": 110, "rank": 1},
        ])

        self.stdout.write(self.style.SUCCESS('Test data successfully populated (pymongo)!'))
