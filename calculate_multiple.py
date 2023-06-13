import qab_batters
import qab_pitchers
import csv
from years import data

year_list = [2022]

player_id_dict = {}

#write data for every PITCHER in the pitcher_ids.csv file
for year in year_list:
    start = str(year) + '-' + str(data[year]['start_date'])
    end = str(year) + '-' + str(data[year]['end_date'])
    with open(f'csv/{year}/pitcher_ids.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['Name']
            player_id = row['PlayerID']
            player_id_dict[name] = player_id

    # Loop over the player IDs dictionary
    for name, player_id in player_id_dict.items():
        qab_pitchers.calculate_qab_percentage(start, end, player_id)




#write data for every BATTER in the hitter_ids.csv file
for year in year_list:
    start = str(year) + '-' + str(data[year]['start_date'])
    end = str(year) + '-' + str(data[year]['end_date'])
    with open(f'csv/{year}/hitter_ids.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['Name']
            player_id = row['PlayerID']
            player_id_dict[name] = player_id

    # Loop over the player IDs dictionary
    for name, player_id in player_id_dict.items():
        qab_batters.calculate_qab_percentage(start, end, player_id)