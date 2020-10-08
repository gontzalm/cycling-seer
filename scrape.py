#!/home/gontz/miniconda3/envs/ih/bin/python3

import click
from src import dbops, procyclingstats


@click.command()
@click.argument("items")
@click.option("-v", "--verbose", is_flag=True)
def scrape(items, verbose):
    """Scrape ITEMS from procyclingstats.com.""" 
    items = items.lower()
    if items not in ["riders", "stages"]:
        raise click.UsageError("ITEMS must be RIDERS or STAGES")

    if items == "riders":
        # TODO Rider names
        for rider in ["alberto-contador", "tadej-pogacar"]:
            rider_data = procyclingstats.get_rider(rider)
            
            # HTTP error
            if isinstance(rider_data, int):
                if verbose:
                    click.echo(f"Cannot get {rider}. Status code: {rider_data}")
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