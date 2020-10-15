#!/home/gontz/miniconda3/envs/ih/bin/python3

import click
import requests
from scipy.stats import mode
from conf import BASE_URL
from src import dbops

@click.command()
def dowload_prof():
    """Download stage profiles from database."""
    stages = dbops.fetch_stages(project=["result", "profile"])
    
    for stage in stages:
        # Get mode of top 10 rider's clusters and set output path
        result = stage["result"]
        clusters = [dbops.fetch_rider(rider)["cluster"] for rider in result]
        cluster = mode(clusters).mode[0]
        path = f"profiles/cluster{cluster}"
    
        # Download profile
        url = f"{BASE_URL}/{stage['profile']}"
        res = requests.get(url)
        f_name = url.split("/")[-1]
        
        with open(f"{path}/{f_name}", "wb") as f:
            f.write(res.content)

        click.echo(f"Downloaded {f_name}")


if __name__ == "__main__":
    dowload_prof()
