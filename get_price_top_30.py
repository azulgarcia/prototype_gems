from app_polygon.update.cb_database_connection import open_connection
import pandas as pd

connection = open_connection()
cursor = connection.cursor(dictionary=True)

all_projects_df = pd.read_csv("all_projects_top_30_General_trim1_2024.csv")

id_project_list = list(set(all_projects_df['id_project'].to_list()))

print(all_projects_df)

category = 'General'
data = []

year = 2024
for id in id_project_list:
    for week in range(1, 14):
        try:
            query_init_price = "select price, DATE(created_at) as created_at from cryptobirds.prices " \
                                "where year(updated_at) = %s and week(updated_at,3) = %s and id_project = %s"
            cursor.execute(query_init_price, (year, week, id))
            price_init_week = cursor.fetchall()
            init_price = float(price_init_week[0]['price'])

            query_end_price = "select price, DATE(created_at) as created_at from cryptobirds.prices " \
                              "where year(updated_at) = %s and week(updated_at,3) = %s and id_project = %s"
            cursor.execute(query_end_price, (year, week+1, id))
            price_last_week = cursor.fetchall()
            end_price = float(price_last_week[0]['price'])

            performance = (end_price - init_price) / init_price

            project_name = all_projects_df.loc[all_projects_df['id_project'] == id, 'name'].iloc[0]

            data.append({'category': category,
                     'date': price_last_week[0]['created_at'],
                     'year': year,
                     'week': week,
                     'id_project': id,
                     'project_name': project_name,
                     'start_price': init_price,
                     'end_price': end_price,
                     'performance': performance
                     })

            print(category, price_last_week[0]['created_at'], year, week, id, project_name,
                  init_price, end_price, performance)
        except:
            print(f'{year}, {week}, Project: {project_name},: has prices problems')


pd.DataFrame(data).to_csv('top_30_performances_trim1_2024_General.csv', sep=',', index=False)