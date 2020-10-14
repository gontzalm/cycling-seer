#!/home/gontz/miniconda3/envs/ih/bin/python3

import click
import requests
from conf import BASE_URL, IMG_DIR
from src import dbops

@click.command()
def dowload_prof():
    """Download stage profiles from database."""
    stages = dbops.fetch_stages(project=["result", "profile"])
    
    for stage in stages:
        # Get winner's cluster and set output path
        winner = stage["result"][0]
        cluster = dbops.fetch_rider(winner)["cluster"]
        path = f"{IMG_DIR}/cluster{cluster}"
    
        # Download profile
        url = f"{BASE_URL}/{stage['profile']}"
        res = requests.get(url)
        f_name = url.split("/")[-1]
        
        with open(f"{path}/{f_name}", "wb") as f:
            f.write(res.content)

        click.echo(f"Downloaded {f_name}")


if __name__ == "__main__":
    dowload_prof()
