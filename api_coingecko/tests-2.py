from app_polygon.update.cb_database_connection import open_connection
import pandas as pd

connection = open_connection()
cursor = connection.cursor(dictionary=True)

df = pd.read_csv("C:/Users/Azul/Desktop/CB/prototype_gems/polygon_coingecko_2_6.csv").reset_index()

for index, row in df.iterrows():
    if row['year'] == 2024 and row['week'] == 1:
        year = 2023
        week = 52
    else:
        year = row['year']
        week = row['week'] - 1

    df.at[index, 'year'] = year
    df.at[index, 'week'] = week
    query_score = "select score from projects_scores where year = %s and week = %s and id_project = %s and top = 'General'"
    cursor.execute(query_score, (year, week, row['id_project']))
    score = cursor.fetchall()
    score = float(score[0]['score'])
    df.at[index, 'score'] = score

    print(row['id_project'], row['project_name'], year, week, score)

df.to_csv('modification_polygon_coningecko.csv', index=False)
