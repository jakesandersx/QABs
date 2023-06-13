import csv
from pybaseball import team_batting_bref, playerid_lookup
import os

mlb_teams = [
    'ARI', 'ATL', 'BAL', 'BOS', 'CHW', 'CHC', 'CIN', 'CLE', 'COL', 'DET',
    'HOU', 'KCR', 'LAA', 'LAD', 'MIA', 'MIL', 'MIN', 'NYY', 'NYM', 'OAK',
    'PHI', 'PIT', 'SDP', 'SFG', 'SEA', 'STL', 'TBR', 'TEX', 'TOR', 'WSN'
]


year_list = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

for year in year_list:
    # Create the directory if it doesn't exist
    directory = f'csv/{year}'
    os.makedirs(directory, exist_ok=True)
    names_list = []

    for team in mlb_teams:
        data = team_batting_bref(team, year)
        data = data[data['Pos'] != 'P']

        # Remove the entries with "(40 man)" and "(10-day IL)" from the Name column
        data['Name'] = data['Name'].str.replace(r'\(40 man\)', '').str.replace(r'\(10-day IL\)', '')

        # Extract only the first two names, except when the name contains "Jr"
        data['Name'] = data['Name'].str.split().apply(lambda x: ' '.join(x[:2]) if not any("Jr" in name for name in x) else ' '.join(x))

        # Select only the "Name" column
        selected_data = data[["Name"]]

        # Append each individual name to the names_list
        names_list.extend(selected_data['Name'].tolist())

        # Print the updated data
        print(selected_data.to_string(index=False, header=(team == mlb_teams[0])))

    player_id_dict = {}
    for full_name in names_list:
        # Split the full name into first name and last name, including "Jr"
        name_parts = full_name.split()
        last_name = name_parts[-1]
        first_name = ' '.join(name_parts[:-1])

        # Use playerid_lookup to get the player ID
        player_ids = playerid_lookup(last_name, first_name)

        # Check if the player ID is found
        if not player_ids.empty:
            # Get the first player ID in the list
            player_id = player_ids['key_mlbam'].values[0]

            # Add the player's name and ID to the dictionary
            player_id_dict[full_name] = player_id

    # Write the dictionary of player names and IDs to a CSV file
    with open(f'{directory}/hitter_ids.csv', 'w', newline='') as csvfile:
        fieldnames = ['Name', 'PlayerID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for name, player_id in player_id_dict.items():
            writer.writerow({'Name': name, 'PlayerID': player_id})

