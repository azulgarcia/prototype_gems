import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

projects_df = pd.read_csv('app_top_monthly/groups_fijo_2.csv')
performances_df = pd.read_csv('app_top_monthly/all_performances.csv')

st.title('Top mensual')
st.write('Top mensual generado a partir de los proyectos con más apariciones en los top 30 semanales '
         'del mes anterior.')
st.write('Por ejemplo, los proyectos incluidos en el top del primer mes, serán los que mayor apariciones tuvieron '
         'en el top 30 de las primeras 4 semanas del año.')
st.write('La cantida de proyectos a considerar en el top mensual, es a elección y puede ser de 10 a 30.')

num_projects = st.slider('Cantidad de proyectos por mes:', 10, 30, 10)

month_map = {5: 'Mes 1', 9: 'Mes 2', 13: 'Mes 3', 17: 'Mes 4'}
projects_df['month'] = projects_df['week_associated'].map(month_map)

unique_months = projects_df['month'].unique()

top_projects_by_month = pd.DataFrame()

for month in unique_months:
    top_projects = projects_df[projects_df['month'] == month].nlargest(num_projects, 'appearance_count')
    top_projects_by_month = pd.concat([top_projects_by_month, top_projects], ignore_index=True)


projects_for_month = top_projects_by_month[['id_project', 'week_associated', 'name']]

new_rows = []
for index, row in projects_for_month.iterrows():
    if row['week_associated'] == 5:
        for i in range(4):
            new_rows.append({'id_project': row['id_project'], 'name': row['name'], 'week_associated': row['week_associated'], 'year': 2024, 'week_performance': row['week_associated'] + i})
    elif row['week_associated'] == 9:
        for i in range(4):
            new_rows.append({'id_project': row['id_project'], 'name': row['name'], 'week_associated': row['week_associated'], 'year': 2024, 'week_performance': row['week_associated'] + i})
    elif row['week_associated'] == 13:
        for i in range(4):
            new_rows.append({'id_project': row['id_project'], 'name': row['name'], 'week_associated': row['week_associated'], 'year': 2024, 'week_performance': row['week_associated'] + i})
    elif row['week_associated'] == 17:
        for i in range(1):
            new_rows.append({'id_project': row['id_project'], 'name': row['name'], 'week_associated': row['week_associated'], 'year': 2024, 'week_performance': row['week_associated'] + i})

expanded_df = pd.DataFrame(new_rows)

performance_values = []
date_performance_values = []
init_prices_values = []
end_prices_values = []

for index, row in expanded_df.iterrows():
    # Filtrar el DataFrame performances_df para obtener la fila correspondiente al proyecto, semana y año
    performance_row = performances_df[(performances_df['id_project'] == row['id_project']) &
                                      (performances_df['week_performance'] == row['week_performance']) &
                                      (performances_df['year'] == row['year'])]

    if not performance_row.empty:
        performance_value = performance_row['performance'].values[0]
        date_performance_value = performance_row['date_performance'].values[0]
        init_price_value = performance_row['init_price'].values[0]
        end_price_value = performance_row['end_price'].values[0]
        performance_values.append(performance_value)
        date_performance_values.append(date_performance_value)
        init_prices_values.append(init_price_value)
        end_prices_values.append(end_price_value)

    else:
        print("errores")
        print(str(row['id_project']) + ", " + str(row['week_performance']))
        performance_values.append(None)
        date_performance_values.append(None)
        init_prices_values.append(None)
        end_prices_values.append(None)


# Agregar las listas como columnas al DataFrame expandido
expanded_df['performance'] = performance_values
expanded_df['date_performance'] = date_performance_values
expanded_df['init_price'] = init_prices_values
expanded_df['end_price'] = end_prices_values



st.markdown('### Rendimiento semanal')

expanded_df['date_performance'] = pd.to_datetime(expanded_df['date_performance']).dt.date
performance_mean = expanded_df.groupby('date_performance')['performance'].mean().reset_index()

init_investment = 1000
roi_total = []
accumulated_roi = init_investment

for index, row in performance_mean.iterrows():
    accumulated_roi = accumulated_roi * (1 + row['performance'])
    roi_total.append(accumulated_roi)

performance_mean['return_total'] = roi_total

fig_roi = px.line(performance_mean, x='date_performance', y='return_total', markers=True, labels={'performance': 'Mean Performance', 'date': 'Date'})
fig_roi.update_traces(line_color='orange')
fig_roi.add_trace(
    go.Scatter(
        x=[performance_mean['date_performance'].min(), performance_mean['date_performance'].max()],
        y=[1000, 1000],
        mode='lines',
        name='Initial Investment',
        line=dict(color="black", width=2, dash="dash"),
    )
)
st.plotly_chart(fig_roi)

st.markdown('### Performance semanal promedio')

fig_performance = px.line(performance_mean, x='date_performance', y='performance',
                          markers=True, labels={'performance': 'Mean Performance', 'date': 'Date'})
fig_performance.update_traces(line_color='green')
st.plotly_chart(fig_performance)


st.markdown('### Proyectos incluidos en el top mensual:')
# Mostrar proyectos del top mensual
selected_month = st.selectbox('Seleccione un mes:', unique_months)
filtered_projects = top_projects_by_month[top_projects_by_month['month'] == selected_month]
st.write("###### Proyectos para el mes seleccionado:")
st.write(filtered_projects[['name', 'appearance_count']])

# Mostrar proyectos del top mensual por semana
unique_weeks = expanded_df['week_performance'].unique()
selected_week = st.selectbox('Seleccione una semana:', unique_weeks)
filtered_projects_week = expanded_df[expanded_df['week_performance'] == selected_week]
st.write("###### Proyectos para la semana seleccionada:")
st.write(filtered_projects_week[['name', 'date_performance', 'init_price', 'end_price', 'performance']])