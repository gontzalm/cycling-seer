#!/home/gontz/miniconda3/envs/ih/bin/python3

import click
from conf import RACES
from itertools import product
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
                    click.echo(f"{rider} inserted with ID: {inserted_id}")
                else:
                    click.echo(f"{rider} already in database.")
    
    else:
        for race, params in RACES.items():
            (start_year, stop_year), no_races = params
            iter_years = range(start_year, stop_year)
            iter_number = range(1, no_races + 1)

            for year, number in product(iter_years, iter_number):
                if verbose:
                    stage = "-".join([race, str(year), str(number)])

                stage_data = procyclingstats.get_stage(race, year, number)
                
                # HTTP error
                if isinstance(stage_data, int):
                    if verbose:
                        click.echo(f"Cannot get {stage}. Status code: {stage_data}")
                    continue

                # Is TTT
                if not stage_data:
                    if verbose:
                        click.echo(f"{stage} is a team time trial. Skipping...")
                    continue

                inserted_id = dbops.insert_stage(stage_data)
                if verbose:
                    if inserted_id:
                        click.echo(f"{stage} inserted with ID: {inserted_id}")
                    else:
                        click.echo(f"{stage} already in database.")


if __name__ == "__main__":
    scrape()