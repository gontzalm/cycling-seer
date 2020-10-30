from src.dbconection import db


def check_exists(elem):
    """Check if element already in database."""
    # Element is rider
    if isinstance(elem, str):
        return bool(db.riders.find_one({"name": elem}))

    # Element is stage
    query = {k: v for k, v in zip(("race", "year", "number"), elem)}
    return bool(db.stages.find_one(query))


def insert_rider(rider):
    """Insert rider in database."""
    oid = db.riders.insert_one(rider).inserted_id
    return str(oid)


def fetch_rider(name):
    """Fetch a single rider from database."""
    return db.riders.find_one({"name": name})


def fetch_riders(project=None):
    """Fetch all riders from database."""
    # Set up projection
    projection = {"_id": 0}
    if project:
        if isinstance(project, list):
            for attr in project:
                projection[attr] = 1
        else:
            projection[project] = 1

    cur = db.riders.find(projection=projection)
    
    # Check if collection is empty
    if cur.count() == 0:
        return None

    return list(cur)


def assign_clusters(df):
    """Assign each rider to its cluster."""
    for rider, cluster in zip(df["name"], df["cluster"]):
        db.riders.update_one({"name": rider}, {"$set": {"cluster": cluster}})


def get_clusters():
    """Get unique clusters."""
    riders = fetch_riders(project="cluster")
    if not riders:
        return None
    return list(set([rider["cluster"] for rider in riders]))


def insert_stage(stage):
    """Insert stage in database."""
    oid = db.stages.insert_one(stage).inserted_id
    return str(oid)    


def fetch_stages(project=None):
    """Fetch all stages from database."""
    # Set up projection
    projection = {"_id": 0}
    if project:
        if isinstance(project, list):
            for attr in project:
                projection[attr] = 1
        else:
            projection[project] = 1

    cur = db.stages.find(projection=projection)

    # Check if collection is empty
    if cur.count() == 0:
        return None

    return list(cur)
