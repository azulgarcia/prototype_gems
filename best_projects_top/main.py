from cb_database_connection import open_connection

year = 2024
week = 10

connection = open_connection()
cursor = connection.cursor(dictionary=True)

query = 'select distinct top from projects_scores where year=%s and week=%s'
cursor.execute(query, (year, week))
tops = cursor.fetchall()

top_names = [top['top'] for top in tops]
print(top_names)

for top in top_names:
    query = 'select id_project from projects_scores where year=%s and week=%s and top=%s ' \
            'order by score desc limit 1'

    cursor.execute(query, (year, week, top))
    project = cursor.fetchall()
    print(top)
    print(project)

