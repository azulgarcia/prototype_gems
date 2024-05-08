import pandas as pd
from cb_database_connection import open_connection

df = pd.read_csv('groups_fijo.csv')

unique_projects_df = df[['id_project']].drop_duplicates()
unique_projects_df = unique_projects_df['id_project'].to_list()

init_week = 5
end_week = 18
year = 2024

connection = open_connection()

# Crear un nuevo DataFrame para almacenar los resultados
result_df = pd.DataFrame(columns=['id_project', 'week_performance', 'year', 'init_price', 'end_price',
                                  'performance', 'date_performance'])

print(unique_projects_df)

for project in unique_projects_df:
    id_project_value = project
    for i in range(init_week, end_week):
        cursor = connection.cursor(dictionary=True)
        try:
            query_price = "select price, created_at from prices " \
                          "where year(created_at)=%s and week(created_at,3)=%s and id_project=%s;"
            cursor.execute(query_price, (int(year), int(i), id_project_value))
            price_init_week = cursor.fetchall()
            init_price = float(price_init_week[0]['price'])

            cursor.execute(query_price, (year, i+1, id_project_value))
            price_end_week = cursor.fetchall()
            end_price = float(price_end_week[0]['price'])

            date_performance = price_end_week[0]['created_at']

            performance = (end_price - init_price) / init_price

            result_df = result_df.append({'id_project': id_project_value,
                                          'week_performance': i,
                                          'year': year,
                                          'init_price': init_price,
                                          'end_price': end_price,
                                          'performance': performance,
                                          'date_performance': date_performance}, ignore_index=True)

            print(str(id_project_value) + ", " + str(i) + ", " + str(year) + ", " +
                  str(init_price) + ", " + str(end_price)+ ", " + str(performance))

        except:
            print('Project: ' + str(id_project_value)
                  + str(i) + ": has prices problems")
        finally:
            cursor.close()

result_df.to_csv('all_performances.csv', index=False)