import qab_batters
import qab_pitchers
import csv
from years import data
from concurrent.futures import ThreadPoolExecutor

year_list = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

def calculate_pitcher_qab(start, end, player_id):
    qab_pitchers.calculate_qab_percentage(start, end, player_id)

def calculate_batter_qab(start, end, player_id):
    qab_batters.calculate_qab_percentage(start, end, player_id)

# Write data for every PITCHER in the pitcher_ids.csv file
for year in year_list:
    start = str(year) + '-' + str(data[year]['start_date'])
    end = str(year) + '-' + str(data[year]['end_date'])
    with open(f'csv/{year}/pitcher_ids.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        player_id_dict = {row['Name']: row['PlayerID'] for row in reader}

    with ThreadPoolExecutor() as executor:
        for name, player_id in player_id_dict.items():
            executor.submit(calculate_pitcher_qab, start, end, player_id)

# Write data for every BATTER in the hitter_ids.csv file
for year in year_list:
    start = str(year) + '-' + str(data[year]['start_date'])
    end = str(year) + '-' + str(data[year]['end_date'])
    with open(f'csv/{year}/hitter_ids.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        player_id_dict = {row['Name']: row['PlayerID'] for row in reader}

    with ThreadPoolExecutor() as executor:
        for name, player_id in player_id_dict.items():
            executor.submit(calculate_batter_qab, start, end, player_id)
