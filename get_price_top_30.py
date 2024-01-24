from cb_database_connection import open_connection
import pandas as pd

connection = open_connection()
cursor = connection.cursor(dictionary=True)

all_projects_df = pd.read_csv("all_projects_top_30_development.csv")

id_project_list = list(set(all_projects_df['id_project'].to_list()))

data = []

## 2024
year = 2024
week = 1
for id in id_project_list:
    try:
        query_init_price = "select price, DATE(created_at) as created_at from cryptobirds.prices " \
                                                   "where year(updated_at) = %s and week(updated_at) = %s and id_project = %s"
        cursor.execute(query_init_price, (2023, 52, id))
        price_init_week = cursor.fetchall()
        init_price = float(price_init_week[0]['price'])

        query_end_price = "select price, DATE(created_at) as created_at from cryptobirds.prices " \
                                                  "where year(updated_at) = %s and week(updated_at) = %s and id_project = %s"
        cursor.execute(query_end_price, (year, week-1, id))
        price_last_week = cursor.fetchall()
        end_price = float(price_last_week[0]['price'])

        performance = (end_price - init_price) / init_price

        project_name = all_projects_df.loc[all_projects_df['id_project'] == id, 'name'].iloc[0]

        data.append({'category': 'Development',
                 'date': price_last_week[0]['created_at'],
                 'year': year,
                 'week': week,
                 'id_project': id,
                 'project_name': project_name,
                 'start_price': init_price,
                 'end_price': end_price,
                 'performance': performance
                 })
        print('Development', price_last_week[0]['created_at'], year, week, id, project_name,
              init_price, end_price, performance)
    except:
        print(f'{year}, {week}, Project: {project_name},: has prices problems')

## 2024 others weeks
year = 2024
for id in id_project_list:
    for week in range(2, 4):
        try:
            query_init_price = "select price, DATE(created_at) as created_at from cryptobirds.prices " \
                                                       "where year(updated_at) = %s and week(updated_at) = %s and id_project = %s"
            cursor.execute(query_init_price, (year, week-2, id))
            price_init_week = cursor.fetchall()
            init_price = float(price_init_week[0]['price'])

            query_end_price = "select price, DATE(created_at) as created_at from cryptobirds.prices " \
                                                      "where year(updated_at) = %s and week(updated_at) = %s and id_project = %s"
            cursor.execute(query_end_price, (year, week-1, id))
            price_last_week = cursor.fetchall()
            end_price = float(price_last_week[0]['price'])

            performance = (end_price - init_price) / init_price

            project_name = all_projects_df.loc[all_projects_df['id_project'] == id, 'name'].iloc[0]

            data.append({'category': 'Development',
                     'date': price_last_week[0]['created_at'],
                     'year': year,
                     'week': week,
                     'id_project': id,
                     'project_name': project_name,
                     'start_price': init_price,
                     'end_price': end_price,
                     'performance': performance
                     })

            print('Development', price_last_week[0]['created_at'], year, week, id, project_name,
                  init_price, end_price, performance)
        except:
            print(f'{year}, {week}, Project: {project_name},: has prices problems')

## 2024 others weeks
year = 2023
for id in id_project_list:
    for week in range(39, 53):
        try:
            query_init_price = "select price, DATE(created_at) as created_at from cryptobirds.prices " \
                                                       "where year(updated_at) = %s and week(updated_at) = %s and id_project = %s"
            cursor.execute(query_init_price, (year, week-1, id))
            price_init_week = cursor.fetchall()
            init_price = float(price_init_week[0]['price'])

            query_end_price = "select price, DATE(created_at) as created_at from cryptobirds.prices " \
                                                      "where year(updated_at) = %s and week(updated_at) = %s and id_project = %s"
            cursor.execute(query_end_price, (year, week, id))
            price_last_week = cursor.fetchall()
            end_price = float(price_last_week[0]['price'])

            performance = (end_price - init_price) / init_price

            project_name = all_projects_df.loc[all_projects_df['id_project'] == id, 'name'].iloc[0]

            data.append({'category': 'Development',
                     'date': price_last_week[0]['created_at'],
                     'year': year,
                     'week': week,
                     'id_project': id,
                     'project_name': project_name,
                     'start_price': init_price,
                     'end_price': end_price,
                     'performance': performance
                     })

            print('Development', price_last_week[0]['created_at'], year, week, id, project_name,
                  init_price, end_price, performance)
        except:
            print(f'{year}, {week}, Project: {project_name},: has prices problems')

pd.DataFrame(data).to_csv('top_30_performances_39_3_development.csv', sep=',', index=False)