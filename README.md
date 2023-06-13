# Major League Baseball Quality At-Bats

# Overview

As a college baseball player myself, we are often graded during our games 
with what are known as `quality at-bats (QABs).` Although it is not a precise
endeavour and can vary from team to team, these are the rules that I have defined for an at-bat to qualify as "Quality":

### Pitcher's Quality At-Bat:
- Strikeout
- Any batted ball with an exit velo less than 80 mph
- Any double play
- Any at-bat with 3 pitches or less that ends in an out

### Hitter's Quality At-Bat:
- Any hit, walk, IBB, or HBP
- Any batted ball with an exit velo of 95+ mph
- Any at-bat with 8 or more pitches seen
- Any at-bat with an RBI



All data is scraped using the `pybaseball` library, which includes Baseball Reference, 
Baseball Savant, and FanGraphs data. A link to pybaseball's github can be found [here](https://github.com/jldbc/pybaseball).

# Requirements
- Python 3.x
- `pybaseball` library

# Installation
1. Clone this repository or download the project as a zip file.

2. Install the required dependencies by running the following command: `pip install pybaseball`

# Usage
1. Import the necessary modules:
```
from pybaseball import statcast_batter
from pybaseball import statcast_pitcher
from prettytable import PrettyTable
```
### Optional Modules

If creating a separate file to get data:
```
import qab_pitchers
import qab_batters
import csv
```

To create your own CSV files:
```
from pybaseball import team_batting_bref
from pybaseball import team_pitching_bref
from pybaseball import playerid_lookup
import csv
```

If interested in storing data via MySQL:
```
import mysql.connector
```
And uncomment all of the MySQL code within the `qab_pitchers.py` and
`qab_batters.py` files. Be sure to also change your `mysql.connector.connect()` data to your corresponding database and table information.

2. Inside of `qab_pitcher.py` or `qab_batter.py`, define the year and player_id you wish to find:
```
year = '2022'
player_id = 592450
```


3. Call the main function: 
```
calculate_qab_percentage(year, player_id)

OR

calculate_qab_percentage('2022', 592450)
```


# Large Dataset Gathering
To gather large amounts of data autonomously, I have also created `calculate_multiple.py` which takes data from the supplied hitter and pitcher csv files, and scrapes data for every entry in the file.
Simply uncomment either bits of the code to scrape data for what you prefer.
Uses `years.py` to automatically get start and end dates of a specified 
year.




# Important Notes:
The data used in these files is Statcast data. Please note that statcast tracks pitch data, therefore
intentional walks are impossible to track, due to no pitches being thrown.
ALL numbers used for hitter's intentional walks are
ESTIMATED using FanGraphs' most recent intentional
walk rate numbers (2021). For more, see [here](https://blogs.fangraphs.com/the-continued-decline-of-the-intentional-walk/)

For this code, data must be used from the 2015 season-onward, as 2015 was the
first season that Statcast began measuring exit velocity, which is used in this measurement.

You might notice that when gathering data, a hitter's RBIs for a season
will not be accurate. However, that is not true. When displaying RBIs, this code
is showing the number of at-bats ending with an RBI, rather than a player's
total number of RBIs for a given season.

All current code is set to correctly retrieve data from the 2022 season.
