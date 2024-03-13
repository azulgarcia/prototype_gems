from api_coingecko.cb_database_connection import open_connection
import pandas as pd

projects = pd.DataFrame(pd.read_csv('data/projects_2024_last.csv'))

projects['created_at'] = pd.to_datetime(projects['created_at'])


connection = open_connection()
cursor = connection.cursor(dictionary=True)

projects['init_price'] = None
projects['end_price'] = None
projects['performance'] = None

for index, row in projects.iterrows():
    id_project = row['id_project']
    year = int(row['year'])
    week = int(row['week'])

    query = "select price, DATE(created_at) as created_at " \
            "from cryptobirds.prices " \
            "where year(updated_at) = %s and week(updated_at) = %s and id_project = %s"

    try:
        cursor.execute(query, (year, week, id_project))
        price_init_week = cursor.fetchall()
        init_price = float(price_init_week[0]['price'])

        if week == 1:
            cursor.execute(query, (year-1, 52, id_project))
        else:
            cursor.execute(query, (year, week-1, id_project))

        price_last_week = cursor.fetchall()
        end_price = float(price_last_week[0]['price'])

        performance = (end_price - init_price) / init_price

        projects.at[index, 'init_price'] = init_price
        projects.at[index, 'end_price'] = end_price
        projects.at[index, 'performance'] = performance

        print(year, week, id_project, init_price, end_price, performance)

    except:
        print(f"missing price {row['name']}, {row['id_project']}, {row['year']}, {row['week']} ")

projects.to_csv('data/projects_with_performance.csv', sep=',', index=False)


projects_monthly = projects.groupby(['id_project', projects['created_at'].dt.month])\
    .agg({'performance': 'mean'}).reset_index()

projects_monthly.rename(columns={'created_at': 'month'}, inplace=True)
df_sorted = projects_monthly.sort_values(by=['month', 'performance'], ascending=[True, False])

top_20_per_month = df_sorted.groupby('month').head(20)

print(top_20_per_month)

top_20_per_month.to_csv('data/top_20_projects_mean_performance_last.csv', sep=',', index=False)
'''
connection = open_connection()
cursor = connection.cursor(dictionary=True)

for index, row in top_20_per_month.iterrows():    
    id_project = row['id_project']    
    query = "select price, DATE(created_at) as created_at " \
            "from cryptobirds.prices " \
            "where year(updated_at) = % s and week(updated_at) = % s and id_project = % s"
    
    cursor.execute(query, (year, week - 2, id_project))
    price_init_week = cursor.fetchall()
    init_price = float(price_init_week[0]['price'])

    cursor.execute(query, (year, week - 1, id))
    price_last_week = cursor.fetchall()
    end_price = float(price_last_week[0]['price'])

    performance = (end_price - init_price) / init_price

'''