import requests
import json
import pandas as pd
from app_polygon.update.cb_database_connection import open_connection


# get projects from the platform
platform = 'polygon-ecosystem'
url = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category={platform}&per_page=100&page=1&sparkline=false&locale=en'
response_api = requests.get(url)
data = response_api.text
parse_json = json.loads(data)
df = pd.DataFrame(parse_json)
list_projects = df['id'].to_list()


# get project id
connection = open_connection()
all_projects_id = []
for id in list_projects:
    try:
        cursor = connection.cursor(dictionary=True)
        sql_select_query = 'select id, name from projects where slug = %s;'
        cursor.execute(sql_select_query, (id,))
        result = cursor.fetchall()
        all_projects_id.append(result)

    finally:
        cursor.close()

print(all_projects_id)
ids = []
names = []

for id in all_projects_id:
    for dicc in id:
        ids.append(dicc['id'])
        names.append(dicc['name'])

df_all_projects = pd.DataFrame({'id': ids, 'name': names})
list_id = df_all_projects['id'].to_list()

connection = open_connection()
platform = 'polygon-ecosystem'
#bitcoin = [[376, 'Bitcoin']]
#df_all_projects = pd.DataFrame(bitcoin, columns=['id', 'name'])
#list_id = df_all_projects['id'].to_list()
print(list_id)
# get price and score general projects
data = []
year = 2024
category = 'General'
current_week = 8

