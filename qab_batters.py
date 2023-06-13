from pybaseball import statcast_batter
import mysql.connector
from prettytable import PrettyTable

def calculate_qab_percentage(start, end, player_id):
    try:
        data = statcast_batter(start, end, player_id=player_id)
        filtered_data = data[data['events'].notna()]

        if len(data) == 0:
            print("No data found for the specified player and year.")
            return

        if "player_name" not in data.columns:
            print("player_name not found in the data.")
            return

        name = data['player_name'].iloc[0]
        ln, fn = name.split(", ")
        new_name = fn + " " + ln

        HHB = filtered_data['launch_speed'] >= 95
        SINGLE = filtered_data['events'] == 'single'
        DOUBLE = filtered_data['events'] == 'double'
        TRIPLE = filtered_data['events'] == 'triple'
        HR = filtered_data['events'] == 'home_run'
        EIGHTPITCH = filtered_data['pitch_number'] >= 8
        BB = filtered_data['events'] == 'walk'
        HBP = filtered_data['events'] == 'hit_by_pitch'
        RBI = filtered_data['des'].str.contains('scores')
        IBB_ESTIMATE = int(len(filtered_data) * 0.003)

        qab = filtered_data[HHB | SINGLE | DOUBLE | TRIPLE | HR | EIGHTPITCH | BB | HBP | RBI]
        at_bats = len(filtered_data) + IBB_ESTIMATE
        selected_columns = ['game_date', 'events', 'des', 'launch_speed', 'pitch_number']
        qab_selected = qab[selected_columns]
        qab_selected = qab_selected.sort_values(by='game_date', ascending=True)

        qab_decimal = len(qab_selected) / at_bats
        qab_percentage = qab_decimal * 100
        formatted_qab_percentage = "{:.2f}".format(qab_percentage)

        hits = sum(SINGLE | DOUBLE | TRIPLE | HR)
        total_qabs = len(qab_selected) + IBB_ESTIMATE

        '''hitters = mysql.connector.connect(
            user='root',
            password='root',
            host='localhost',
            database='qab_data',
            auth_plugin='mysql_native_password'
        )

        # Insert data into MySQL database
        cursor = hitters.cursor()
        insert_data = "INSERT INTO hitters(playerid, player_name, year, qab, pa, qab_percentage, hits, bb, est_ibb, hbp, 8pitches, RBI, barrels) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        qab_data = (player_id, new_name, start[0:4], total_qabs, at_bats, formatted_qab_percentage, hits, sum(BB), IBB_ESTIMATE, sum(HBP), sum(EIGHTPITCH), sum(RBI), sum(HHB))
        cursor.execute(insert_data, qab_data)
        hitters.commit()
        hitters.close()'''

        # Print table of all columns and data
        table = PrettyTable()
        table.field_names = ['Player', 'Year', 'QABs', 'PAs', 'QAB_%', 'Hits', 'BB', 'EST_IBB', 'HBP', '8PitchAB', 'RBI', 'Barrels']
        table.add_row([new_name, start[0:4], total_qabs, at_bats, formatted_qab_percentage, hits, sum(BB), IBB_ESTIMATE, sum(HBP),sum(EIGHTPITCH), sum(RBI), sum(HHB)])
        print(table)
    except Exception as e:
        print(e)


'''
if using calculate_mulitple.py,
comment out this function call
'''
calculate_qab_percentage('2022', 592450)