from src.dbconection import db


def insert_rider(rider):
    """Insert rider in database."""
    # Check if rider in db
    if db.riders.find_one({"name": rider["name"]}):
        return None

    oid = db.riders.insert_one(rider).inserted_id
    return str(oid)


def fetch_riders():
    """Fetch all riders from database."""
    cur = db.riders.find()
    
    # Check if collection is empty
    if cur.count() == 0:
        return None

    return list(cur)


def insert_stage(stage):
    """Insert stage in database."""
    # Check if stage in db
    query = {k: stage[k] for k in ["race", "year", "number"]}
    if db.stages.find_one(query):
        return None

    oid = db.stages.insert_one(stage).inserted_id
    return str(oid)    


def fetch_stages():
    """Fetch all stages from database."""
    cur = db.stages.find()

    # Check if collection is empty
    if cur.count() == 0:
        return None

    return list(cur)
