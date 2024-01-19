import pandas as pd

df = pd.read_csv('all_categories_performance.csv')
df['date'] = pd.to_datetime(df['date'])

category_filter = ['Gems', 'Gems<15', 'Gems<25']
filtered_df = df[df['category'].isin(category_filter)]

year_filter = [2023, 2024]
filtered_df = filtered_df[filtered_df['date'].dt.year.isin(year_filter)]
filtered_df['date'] = pd.to_datetime(filtered_df['date']).dt.date

df_filtrado = filtered_df.groupby(['category', 'date'])['performance'].mean().reset_index()

file_name = 'performances_by_category.csv'
df_filtrado.to_csv(file_name, sep=',', index=False)
