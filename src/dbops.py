from src.dbconection import db


def check_exists(elem):
    """Check if element already in database."""
    # Element is rider
    if isinstance(elem, str):
        if db.riders.find_one({"name": elem}):
            return True
        else:
            return False

    # Elemet is stage
    query = {k: v for k, v in zip(("race", "year", "number"), elem)}
    if db.stages.find_one(query):
        return True
    else:
        return False


def insert_rider(rider):
    """Insert rider in database."""
    oid = db.riders.insert_one(rider).inserted_id
    return str(oid)


def fetch_riders():
    """Fetch all riders from database."""
    cur = db.riders.find(projection={"_id": 0})
    
    # Check if collection is empty
    if cur.count() == 0:
        return None

    return list(cur)


def insert_stage(stage):
    """Insert stage in database."""
    oid = db.stages.insert_one(stage).inserted_id
    return str(oid)    


def fetch_stages(project=None):
    """Fetch all stages from database."""
    # Set up projection
    projection = {"_id": 0}
    if project:
        projection[project] = 1

    cur = db.stages.find(projection=projection)

    # Check if collection is empty
    if cur.count() == 0:
        return None

    return list(cur)
