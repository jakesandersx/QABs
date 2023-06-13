from pybaseball import statcast_pitcher
import mysql.connector
from prettytable import PrettyTable

def calculate_qab_percentage(start, end, player_id):
    try:
        data = statcast_pitcher(start, end, player_id = player_id)
        filtered_data = data[data['events'].notna()]

        if len(data) == 0:
            print("no data found for specified player and year")
            return

        if "player_name" not in data.columns:
            print("player_name not found in the data")
            return

        name = data['player_name'].iloc[0]
        ln, fn = name.split(", ")
        new_name = fn + " " + ln

        SOFT = filtered_data['launch_speed'] <= 80
        THREEPITCH = filtered_data['pitch_number'] <= 3 & filtered_data['events'].str.contains('out')
        K = filtered_data['events'] == 'strikeout'
        DP = filtered_data['events'].str.contains('double_play')

        qab = filtered_data[SOFT | THREEPITCH | K | DP]
        bf = len(filtered_data)

        qab_decimal = len(qab) / bf
        qab_percentage = qab_decimal * 100
        formatted_qab_percentage = "{:.2f}".format(qab_percentage)

        total_qabs = len(qab)

        '''pitchers = mysql.connector.connect(
                    user='root',
                    password='root',
                    host='localhost',
                    database='qab_data',
                    auth_plugin='mysql_native_password'
                )


        cursor = pitchers.cursor()
        insert_data = "INSERT INTO pitchers(player_name, year, qab, bf, qab_percentage, strikeouts, soft_contact, 3pitch, double_plays) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        qab_data = (new_name, start[0:4], total_qabs, bf, formatted_qab_percentage, sum(K), sum(SOFT), sum(THREEPITCH), sum(DP))
        cursor.execute(insert_data, qab_data)
        pitchers.commit()
        pitchers.close()'''

        table = PrettyTable()
        table.field_names = ['Player', 'Year', 'QABs', 'BF', 'QAB_%', 'Strikeouts', 'Soft Contact', '3PitchABs', 'DPs']
        table.add_row([new_name, start[0:4], total_qabs, bf, formatted_qab_percentage, sum(K), sum(SOFT), sum(THREEPITCH), sum(DP),])
        print(table)
    except Exception as e:
        print(e)


'''
if using calculate_mulitple.py,
comment out this function call
'''
calculate_qab_percentage('2022', 675912)