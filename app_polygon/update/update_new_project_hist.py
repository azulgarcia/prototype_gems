import requests
import json
import pandas as pd
from cb_database_connection import open_connection


# historico nuevos proyectos
total_db = pd.read_csv('/app_polygon/modification_polygon_coningecko.csv')
current_projects = pd.read_csv('/polygon_coingecko_current.csv')
list_id_total = total_db['id_project'].unique().tolist()
list_current = current_projects['id_project'].tolist()
data_new_projects = []

connection = open_connection()
category = 'General'
platform = 'polygon-ecosystem'
current_week = 10

print('HISTORICO NUEVOS PROYECTOS')
for id in list_current:
    if id in list_id_total:
        pass
    else:
        # 2023
        for week in range(6, 52):
            cursor = connection.cursor(dictionary=True)
            project_name = current_projects.loc[current_projects['id_project'] == id, 'project_name'].iloc[0]
            try:
                query_init_price = "select a.id_project, week, score, year, price, b.created_at from projects_scores a left join prices b " \
                                   "on a.id_project = b.id_project and a.year = year(b.created_at) and a.week=week(b.created_at,3)" \
                                   "where a.id_project = %s and year = %s and week = %s and top = %s;"
                cursor.execute(query_init_price, (id, 2023, week, category))
                price_init_week = cursor.fetchall()
                init_price = float(price_init_week[0]['price'])

                query_end_price = "select a.id_project, week, score, year, price, b.created_at from projects_scores a left join prices b " \
                                  "on a.id_project = b.id_project and a.year = year(b.created_at) and a.week=week(b.created_at,3)" \
                                  "where a.id_project = %s and year = %s and week = %s and top = %s;"
                cursor.execute(query_end_price, (id, 2023, week+1, category))
                price_last_week = cursor.fetchall()
                end_price = float(price_last_week[0]['price'])
                performance = (end_price - init_price) / init_price

                score = float(price_init_week[0]['score'])

                data_new_projects.append({'category': category,
                                       'platform': platform,
                                       'date': price_last_week[0]['created_at'],
                                       'year': 2023,
                                       'week': week,
                                       'id_project': id,
                                       'project_name': project_name,
                                       'start_price': init_price,
                                       'end_price': end_price,
                                       'performance': performance,
                                       'score': score,
                                       })
                print(category, price_last_week[0]['created_at'], 2023, week, id, project_name,
                      init_price, end_price, performance)
            except:
                print(f'{2023}, {week}, Project: {project_name},: has prices problems')

        # semana 52 2023
        for week in range(52, 53):
            cursor = connection.cursor(dictionary=True)
            project_name = current_projects.loc[current_projects['id_project'] == id, 'project_name'].iloc[0]
            try:
                query_init_price = "select a.id_project, week, score, year, price, b.created_at from projects_scores a left join prices b " \
                                   "on a.id_project = b.id_project and a.year = year(b.created_at) and a.week=week(b.created_at,3)" \
                                   "where a.id_project = %s and year = %s and week = %s and top = %s;"
                cursor.execute(query_init_price, (id, 2023, week, category))
                price_init_week = cursor.fetchall()
                init_price = float(price_init_week[0]['price'])

                query_end_price = "select a.id_project, week, score, year, price, b.created_at from projects_scores a left join prices b " \
                                  "on a.id_project = b.id_project and a.year = year(b.created_at) and a.week=week(b.created_at,3)" \
                                  "where a.id_project = %s and year = %s and week = %s and top = %s;"
                cursor.execute(query_end_price, (id, 2024, 1, category))
                price_last_week = cursor.fetchall()
                end_price = float(price_last_week[0]['price'])
                performance = (end_price - init_price) / init_price

                score = float(price_init_week[0]['score'])

                data_new_projects.append({'category': category,
                                       'platform': platform,
                                       'date': price_last_week[0]['created_at'],
                                       'year': 2023,
                                       'week': week,
                                       'id_project': id,
                                       'project_name': project_name,
                                       'start_price': init_price,
                                       'end_price': end_price,
                                       'performance': performance,
                                       'score': score,
                                       })
                print(category, price_last_week[0]['created_at'], 2023, week, id, project_name,
                      init_price, end_price, performance)
            except:
                print(f'{2023}, {week}, Project: {project_name},: has prices problems')

        # 2024
        for week in range(1, current_week):
            cursor = connection.cursor(dictionary=True)
            project_name = current_projects.loc[current_projects['id_project'] == id, 'project_name'].iloc[0]
            try:
                query_init_price = "select a.id_project, week, score, year, price, b.created_at from projects_scores a left join prices b " \
                                   "on a.id_project = b.id_project and a.year = year(b.created_at) and a.week=week(b.created_at,3)" \
                                   "where a.id_project = %s and year = %s and week = %s and top = %s;"
                cursor.execute(query_init_price, (id, 2024, week, category))
                price_init_week = cursor.fetchall()
                init_price = float(price_init_week[0]['price'])

                query_end_price = "select a.id_project, week, score, year, price, b.created_at from projects_scores a left join prices b " \
                                  "on a.id_project = b.id_project and a.year = year(b.created_at) and a.week=week(b.created_at,3)" \
                                  "where a.id_project = %s and year = %s and week = %s and top = %s;"
                cursor.execute(query_end_price, (id, 2024, week+1, category))
                price_last_week = cursor.fetchall()
                end_price = float(price_last_week[0]['price'])
                performance = (end_price - init_price) / init_price

                score = float(price_init_week[0]['score'])

                data_new_projects.append({'category': category,
                                       'platform': platform,
                                       'date': price_last_week[0]['created_at'],
                                       'year': 2024,
                                       'week': week,
                                       'id_project': id,
                                       'project_name': project_name,
                                       'start_price': init_price,
                                       'end_price': end_price,
                                       'performance': performance,
                                       'score': score,
                                       })
                print(category, price_last_week[0]['created_at'], 2024, week, id, project_name,
                      init_price, end_price, performance)
            except:
                print(f'{2024}, {week}, Project: {project_name},: has prices problems')

pd.DataFrame(data_new_projects).to_csv(f'performance_new_projects_polygon_{current_week - 1}.csv', sep=',', index=True)






