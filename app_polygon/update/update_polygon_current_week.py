import requests
import json
import pandas as pd
from cb_database_connection import open_connection


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
current_week = 18

# BUSQUEDA DE TOP ACTUAL CON PRECIO DE INICIO
for id in list_id:
    for week in range(current_week, current_week+1):
        cursor = connection.cursor(dictionary=True)
        project_name = df_all_projects.loc[df_all_projects['id'] == id, 'name'].iloc[0]
        try:
            query_init_price = "select a.id_project, week, score, year, price, b.created_at from projects_scores a left join prices b " \
                               "on a.id_project = b.id_project and a.year = year(b.created_at) and a.week=week(b.created_at,3)" \
                               "where a.id_project = %s and year = %s and week = %s and top = %s;"
            cursor.execute(query_init_price, (id, year, week, category))
            price_init_week = cursor.fetchall()
            init_price = float(price_init_week[0]['price'])

            end_price = '-'
            performance = '-'

            score = float(price_init_week[0]['score'])

            data.append({'category': category,
                         'platform': platform,
                         'date': price_init_week[0]['created_at'],
                         'year': year,
                         'week': week,
                         'id_project': id,
                         'project_name': project_name,
                         'start_price': init_price,
                         'end_price': end_price,
                         'performance': performance,
                         'score': score,
                         })
            print(category, price_init_week[0]['created_at'], year, week, id, project_name,
                  init_price, end_price, performance)
        except:
            print(f'{year}, {week}, Project: {project_name},: has prices problems')

pd.DataFrame(data).to_csv(f'data/current_week_polygon_{current_week}.csv', sep=',', index=False)

