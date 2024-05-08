from app_polygon.update.cb_database_connection import open_connection
import pandas as pd

def fetch_data (connection, year, week, category, platform, limit_top):
     query = 'select id_project, name, score, position, platform, year, week ' \
                 'from cryptobirds.projects_scores a ' \
                 'left join cryptobirds.projects b on a.id_project = b.id ' \
                 'where year = %s and week = %s and top = %s and platform = %s ' \
                 'order by score desc limit %s;'

     cursor = connection.cursor(dictionary=True)
     cursor.execute(query, (year, week, category, platform, limit_top))

     return pd.DataFrame(cursor.fetchall())


connection = open_connection()

category = 'Gems'
platform = 'ethereum'
field_platform_name = 'Ethereum'
limit_top = 10
year = 2023
data = []


for week in range(52, 53):
    projects = fetch_data(connection, year, week-1, category, platform, limit_top)
    #all_prorjects_df = pd.concat([all_prorjects_df, projects], ignore_index=True)

    for id_project in projects['id_project'].to_list():
        cursor = connection.cursor(dictionary=True)
        project_name = projects.loc[projects['id_project'] == id_project, 'name'].iloc[0]

        try:
            query_init_price = "select price, DATE(created_at) as created_at from cryptobirds.prices " \
                               "where year(updated_at) = %s and week(updated_at) = %s and id_project = %s"
            cursor.execute(query_init_price, (year, week-1, id_project))
            price_init_week = cursor.fetchall()
            init_price = float(price_init_week[0]['price'])

            query_end_price = "select price, DATE(created_at) as created_at from cryptobirds.prices " \
                              "where year(updated_at) = %s and week(updated_at) = %s and id_project = %s"
            cursor.execute(query_end_price, (year, week, id_project))
            price_last_week = cursor.fetchall()
            end_price = float(price_last_week[0]['price'])

            performance = (end_price - init_price) / init_price


            data.append({'category': category,
                         'platform': field_platform_name,
                         'date': price_last_week[0]['created_at'],
                         'year': year,
                         'week': week,
                         'id_project': id_project,
                         'project_name': project_name,
                         'start_price': init_price,
                         'end_price': end_price,
                         'performance': performance
                         })
            print(category, price_last_week[0]['created_at'], year, week, id_project, project_name,
                  init_price, end_price, performance)
        except:
            print(f'{year}, {week}, Project: {project_name},: has prices problems')

print(data)
pd.DataFrame(data).to_csv('top_10_performances_ethereum_gems_52.csv', sep=',', index=False)


