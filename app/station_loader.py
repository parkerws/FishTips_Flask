import json
import sqlite3
import requests


url = 'https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json?type=waterlevels&units=english'
content = requests.get(url).content
data = json.loads(content)
cleaned_data = []

for row in data['stations']:
    data = (str(row['id']), str(row['state']), str(row['name']), str(row['timezone']), float(row['lat']), float(row['lng']))
    cleaned_data.append(data)

try:
    db = sqlite3.connect('../app.db')
    cursor = db.cursor()
    cursor.executemany('insert into station(station_id, state, name, timezone, lat, long) values(?,?,?,?,?,?)', cleaned_data)
except Exception as E:
    print('Error  :', E)
else:
    db.commit()
    print('data inserted')