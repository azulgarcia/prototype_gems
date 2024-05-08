import pandas as pd

df = pd.read_csv('results_with_performances.csv')

unique_projects_df = df[['id_project', 'name']].drop_duplicates()

grouped_df = df.groupby(['week_associated', 'id_project']).agg({
    'performance': ['count', 'mean'],  # Calcula la cantidad de apariciones y la media de performance para cada grupo
    'score': 'mean'  # Calcula el promedio de score para cada grupo
}).reset_index()

grouped_df.columns = ['week_associated', 'id_project', 'appearance_count', 'performance_mean', 'score_mean']

grouped_df = pd.merge(grouped_df, unique_projects_df, on='id_project', how='left')

week_associated_filter = [5, 9, 13, 17]

filtered_grouped_df = grouped_df.loc[grouped_df['week_associated'].isin(week_associated_filter)].copy()

week_date_map = {
    5: '2024-03-04',
    9: '2024-03-31',
    13: '2024-04-29',
    17: '2024-05-27'
}

filtered_grouped_df['date'] = filtered_grouped_df['week_associated'].map(week_date_map)

filtered_grouped_df.to_csv('groups_fijo_2.csv', index=False)
