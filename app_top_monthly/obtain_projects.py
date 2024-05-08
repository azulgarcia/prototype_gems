from cb_database_connection import open_connection
import pandas as pd

init_week = 5
end_week = 19
year = 2024

connection = open_connection()

results_list = []

for week in range(init_week, end_week):
    print("For week "+str(week)+":")
    for i in range(week-4, week):
        try:
            print(i)
            cursor = connection.cursor(dictionary=True)
            sql_select_query = 'select id_project,week,year,top,score,a.created_at,name from projects_scores a inner join projects b on a.id_project = b.id where year = %s and week = %s and top = "General" order by score desc limit 30;'
            cursor.execute(sql_select_query, (year, i))
            result = cursor.fetchall()

            for res in result:
                res['week_associated'] = week
                results_list.append(res)

        finally:
            cursor.close()

df = pd.DataFrame(results_list)
df.to_csv('results.csv')

print("Searching performances")
for index, row in df.iterrows():
    week_value = row['week']
    id_project_value = row['id_project']
    year_value = row['year']

    cursor = connection.cursor(dictionary=True)

    try:
        query_price = "select price, created_at from prices where year(created_at)=%s and week(created_at,3)=%s and id_project=%s;"
        cursor.execute(query_price, (year_value,week_value,id_project_value))
        price_init_week = cursor.fetchall()
        init_price = float(price_init_week[0]['price'])

        cursor.execute(query_price, (year_value, week_value+1, id_project_value))
        price_end_week = cursor.fetchall()
        end_price = float(price_end_week[0]['price'])

        date_performance = price_end_week[0]['created_at']

        performance = (end_price - init_price) / init_price

        df.at[index, 'init_price'] = init_price
        df.at[index, 'end_price'] = end_price
        df.at[index, 'performance'] = performance
        df.at[index, 'date_performance'] = date_performance

        print(row['name'], row['id_project'], row['week'], row['year'], init_price, end_price, performance)

    except:
        print('Project: ' + str(row['name']) + str(row['id_project'])
              + str(row['week']) + ": has prices problems")

    finally:
        cursor.close()

df.to_csv('results_with_performances.csv')