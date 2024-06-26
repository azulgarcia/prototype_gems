from app_polygon.update.cb_database_connection import open_connection
import pandas as pd
'''
1. Generar proyectos del top 30 general de los últimos 3 meses (este script).
2. Buscar precios de los proyectos generados en el paso 1 (script get_price_top_30.py).
3. Modificar fechas y nombres de archivos en la app (Top_30_General.py).
'''

def fetch_data (connection, year, week, category, limit_top):
    query_end_price = "SELECT id_project, name, top, score, year, week " \
                      "FROM cryptobirds.projects_scores as a left join cryptobirds.projects as b " \
                      "ON a.id_project = b.id where a.year = %s and a.week = %s and a.top = %s " \
                      "order by a.score desc limit %s;"

    cursor = connection.cursor(dictionary=True)
    cursor.execute(query_end_price, (year, week, category, limit_top))

    return pd.DataFrame(cursor.fetchall())

'''
all_projects_df = pd.read_csv("all_projects_top_30.csv")

project_week_counts = all_projects_df.groupby('name')['week'].nunique().reset_index()

project_week_counts = project_week_counts.rename(columns={'week': 'weeks_count'})

#bitcoin = project_week_counts[project_week_counts['name'] == 'Bitcoin']

project_week_counts_sorted = project_week_counts.sort_values(by='weeks_count', ascending=False)
print(project_week_counts_sorted)
'''

connection = open_connection()

all_prorjects_df = pd.DataFrame()

category = 'General'
limit_top = 30

### projects year 2024
for week in range(1, 15):
    projects = fetch_data(connection, 2024, week, category, limit_top)
    all_prorjects_df = pd.concat([all_prorjects_df, projects], ignore_index=True)


print(all_prorjects_df)
all_prorjects_df.to_csv("all_projects_top_30_General_trim1_2024.csv")
connection.close()
