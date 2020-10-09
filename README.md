# cycling-seer
Final project.


## Scraping
```bash
(base) gontz@miair13:~/ironhack/myprojects/cycling-seer$ ./scrape.py --help
Usage: scrape.py [OPTIONS] ITEMS

  Scrape ITEMS from procyclingstats.com.

Options:
  -v, --verbose
  --help         Show this message and exit.
```
Example:
```bash
(base) gontz@miair13:~/ironhack/myprojects/cycling-seer$ ./scrape.py -v stages
['vuelta-a-espana', 2019, 20] inserted with ID: 5f80163e50b3e70556f5324a
['vuelta-a-espana', 2019, 21] inserted with ID: 5f80164150b3e70556f5324b
['tirreno-adriatico', 2019, 1] is a team time trial. Skipping...
['tirreno-adriatico', 2019, 2] inserted with ID: 5f80164450b3e70556f5324c
['tirreno-adriatico', 2019, 3] inserted with ID: 5f80164650b3e70556f5324d
['tirreno-adriatico', 2019, 4] inserted with ID: 5f80164850b3e70556f5324e
['tirreno-adriatico', 2019, 5] inserted with ID: 5f80164a50b3e70556f5324f
['tirreno-adriatico', 2019, 6] inserted with ID: 5f80164c50b3e70556f53250
['tirreno-adriatico', 2019, 7] inserted with ID: 5f80164d50b3e70556f53251
['tirreno-adriatico', 2019, 8] could not be retrieved. Status code: 404
['tirreno-adriatico', 2020, 1] inserted with ID: 5f80165050b3e70556f53252
```