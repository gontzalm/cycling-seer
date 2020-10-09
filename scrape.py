#!/home/gontz/miniconda3/envs/ih/bin/python3

from itertools import product
import click
from conf import RACES
from src import dbops, procyclingstats


@click.command()
@click.argument("items")
@click.option("-v", "--verbose", is_flag=True)
def scrape(items, verbose):
    """Scrape ITEMS from procyclingstats.com."""
    items = items.lower()

    # Invalid argument
    if items not in ["riders", "stages"]:
        raise click.UsageError("ITEMS must be STAGES or RIDERS")

    # Scrape stages
    if items == "stages":
        for race, params in RACES.items():
            (start_year, stop_year), no_races = params
            iter_years = range(start_year, stop_year)
            iter_number = range(1, no_races + 1)

            for year, number in product(iter_years, iter_number):
                stage = [race, year, number]
                if dbops.check_exists(stage):
                    if verbose:
                        click.echo(f"{stage} already in database.")
                    continue

                stage_data = procyclingstats.get_stage(race, year, number)

                # HTTP error
                if isinstance(stage_data, int):
                    if verbose:
                        click.echo(f"{stage} could not be retrieved. Status code: {stage_data}")
                    continue

                # Is TTT
                if not stage_data:
                    if verbose:
                        click.echo(f"{stage} is a team time trial. Skipping...")
                    continue

                inserted_id = dbops.insert_stage(stage_data)
                if verbose:
                    click.echo(f"{stage} inserted with ID: {inserted_id}")

    # Srape riders
    else:
        stages = dbops.fetch_stages(project="result")
        riders = [rider for stage in stages for rider in stage["result"]]

        for rider in riders:
            if dbops.check_exists(rider):
                if verbose:
                    click.echo(f"{rider} already in database.")
                continue

            rider_data = procyclingstats.get_rider(rider)

            # HTTP error
            if isinstance(rider_data, int):
                if verbose:
                    click.echo(f"{rider} could not be retrieved. Status code: {rider_data}")
                continue

            inserted_id = dbops.insert_rider(rider_data)
            if verbose:
                click.echo(f"{rider} inserted with ID: {inserted_id}")


if __name__ == "__main__":
    scrape()
    