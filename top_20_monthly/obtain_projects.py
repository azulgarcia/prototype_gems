from app_polygon.update.cb_database_connection import open_connection
import pandas as pd

def get_projects(year, week, category, limit_top):
    query = "SELECT id_project, name, top, score, year, week, a.created_at " \
            "FROM cryptobirds.projects_scores as a left join cryptobirds.projects as b " \
            "ON a.id_project = b.id where a.year = %s and a.week = %s and a.top = %s " \
            "order by a.score desc limit %s;"

    cursor.execute(query, (year, week, category, limit_top))
    projects = pd.DataFrame(cursor.fetchall())

    return projects


connection = open_connection()
cursor = connection.cursor(dictionary=True)

year = 2024
category = "General"
limit_top = 50

all_projects_df = pd.DataFrame()

for week in range(5, 9):
    all_projects_df = pd.concat([all_projects_df, get_projects(year, week, category, limit_top)], ignore_index=True)

all_projects_df.to_csv('data/projects_2024_last.csv', sep=',', index=False)