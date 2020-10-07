from src.dbconection import db


def insert_rider(rider):
    """Insert rider in database."""
    # Check if rider in db
    query = {"name": rider["name"], "lname": rider["lname"]}
    if db.riders.find_one(query):
        return None

    # Insert rider
    oid = db.riders.insert_one(rider).inserted_id
    return str(oid)


def fetch_riders():
    """Fetch all riders from database."""
    cur = db.riders.find()
    
    # Check if collection is empty
    if cur.count() == 0:
        return None

    return list(cur)


def insert_race(race):
    """Insert race in database."""
    query = {}
    pass


def fetch_races():
    """Fetch all races from database."""
    pass