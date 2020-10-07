#!/home/gontz/miniconda3/envs/ih/bin/python3

import click
from src import dbops, procyclingstats


@click.command()
@click.argument("item")
@click.option("-v", "--verbose", is_flag=True)
def scrape(item, verbose):
    """Scrape ITEMs from procyclingstats.com.""" 
    item = item.lower()
    if item not in ["rider", "race"]:
        raise click.UsageError("ITEM must be RIDER or RACE")

    if item == "rider":
        for rider in ["alberto-contador", "tadej-pogacar"]:
            rider_data = procyclingstats.get_rider(rider)
            
            # HTTP error
            if not rider_data:
                if verbose:
                    print(f"Something went wrong when getting {rider}")
                continue
            
            inserted_id = dbops.insert_rider(rider_data)
            if verbose:
                if inserted_id:
                    click.echo(f"Rider {rider} inserted with ID: {inserted_id}")
                else:
                    click.echo(f"Rider {rider} already in database.")
    
    else:
        pass
            

if __name__ == "__main__":
    scrape()