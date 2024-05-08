import pandas as pd

df = pd.read_csv("modification_polygon_coningecko.csv", delimiter=',', encoding='utf8')

current_year = 2024
current_week = 18

df = df[(df['year'] == current_year) & (df['week'] == current_week-1)]

df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')


def top_10_projects(df):
    return df.nlargest(10, 'score')

top_10_df = df.groupby('date', group_keys=False).apply(top_10_projects)

print(top_10_df)


top_10_df = top_10_df[['platform', 'date', 'year', 'week', 'id_project', 'project_name', 'start_price', 'end_price',
        'performance']]

top_10_df['week'] = top_10_df['week'] + 1

top_10_df.to_csv(f'polygon_premium_{current_week}.csv', index=False)