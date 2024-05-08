import pandas as pd
from cb_database_connection import open_connection

connection = open_connection()
platform = 'polygon-ecosystem'

#Cierre ultima semana
current_week = 18
year = 2024
category = 'General'
data_last_week = []
projects_last_week = pd.read_csv('../polygon_coingecko_current.csv')
list_projects_last_week = projects_last_week['id_project'].to_list()
print('CIERRE ULTIMA SEMANA')
for id in list_projects_last_week:
    for week in range(current_week-1, current_week):
        cursor = connection.cursor(dictionary=True)
        project_name = projects_last_week.loc[projects_last_week['id_project'] == id, 'project_name'].iloc[0]
        try:
            query_init_price = "select a.id_project, week, score, year, price, b.created_at from projects_scores a left join prices b " \
                               "on a.id_project = b.id_project and a.year = year(b.created_at) and a.week=week(b.created_at,3)" \
                               "where a.id_project = %s and year = %s and week = %s and top = %s;"
            cursor.execute(query_init_price, (id, year, week, category))
            price_init_week = cursor.fetchall()
            init_price = float(price_init_week[0]['price'])

            query_end_price = "select a.id_project, week, score, year, price, b.created_at from projects_scores a left join prices b " \
                              "on a.id_project = b.id_project and a.year = year(b.created_at) and a.week=week(b.created_at,3)" \
                             "where a.id_project = %s and year = %s and week = %s and top = %s;"
            cursor.execute(query_end_price, (id, year, week+1, category))
            price_last_week = cursor.fetchall()
            end_price = float(price_last_week[0]['price'])
            performance = (end_price - init_price) / init_price

            score = float(price_init_week[0]['score'])

            data_last_week.append({'category': category,
                         'platform': platform,
                         'date': price_last_week[0]['created_at'],
                         'year': year,
                         'week': week,
                         'id_project': id,
                         'project_name': project_name,
                         'start_price': init_price,
                         'end_price': end_price,
                         'performance': performance,
                         'score': score,
                         })
            print(category, price_last_week[0]['created_at'], year, week, id, project_name,
                  init_price, end_price, performance)
        except:
            print(f'{year}, {week}, Project: {project_name},: has prices problems')

pd.DataFrame(data_last_week).to_csv(f'data/performance_last_week_polygon_{current_week-1}.csv', sep=',', index=True)
