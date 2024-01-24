import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

df_top = pd.read_csv("all_projects_top_39_3.csv")

df = pd.read_csv('top_30_performances_39_3.csv')
df['date'] = pd.to_datetime(df['date'])

###############################################################################################################
# Performance for date
###############################################################################################################

df['date'] = pd.to_datetime(df['date']).dt.date

print(df.columns)

st.title('Top 30 General')
st.write('Period: 09/24/2023 to 01/20/2024')
st.write('Number of weeks analyzed: 17')
###############################################################################################################
# Apariciones de los proyectos
###############################################################################################################
project_week_counts = df_top.groupby('name')['week'].nunique().reset_index()
project_week_counts = project_week_counts.rename(columns={'week': 'weeks_count'})
project_week_counts_sorted = project_week_counts.sort_values(by='weeks_count', ascending=False)
project_week_counts_sorted = project_week_counts_sorted.reset_index(drop=True)

num_projects_to_show = st.number_input("Enter number of projects", min_value=1, max_value=len(project_week_counts_sorted), value=30)
top_projects = project_week_counts_sorted.head(num_projects_to_show)

top_projects_2 = top_projects.rename(columns={'name': 'Project', 'weeks_count': 'Number of weeks'})

st.table(top_projects_2.set_index('Project'))

###############################################################################################################
# Streamlit app
###############################################################################################################

st.markdown('### Performances selected projects')

rango_fechas = pd.date_range(df['date'].min(), df['date'].max())
fecha_inicio_default = max(rango_fechas.min().date(), df['date'].min())  # Establecer un valor predeterminado dentro del rango
fecha_fin_default = min(rango_fechas.max().date(), df['date'].max())  # Establecer un valor predeterminado dentro del rango
fecha_inicio = st.date_input("Select start date",
                             min_value=rango_fechas.min().date(),
                             max_value=rango_fechas.max().date(),
                             value=fecha_inicio_default)
fecha_fin = st.date_input("Select end date",
                          min_value=rango_fechas.min().date(),
                          max_value=rango_fechas.max().date(),
                          value=fecha_fin_default)

df_filtrado = df[(df['date'] >= fecha_inicio) & (df['date'] <= fecha_fin)]

#df_filtrado = df_filtrado.groupby(['project_name', 'date'])['performance'].mean().reset_index()

selected_projects = top_projects['name'].tolist()

df_filtrado = df_filtrado[df_filtrado['project_name'].isin(selected_projects)]

st.table(df_filtrado.sort_values(by='date', ascending=True))

grouped_df = df_filtrado.groupby('date')['performance'].mean().reset_index()


init_investment = 1000
roi_total = []

accumulated_roi = init_investment
for index, row in grouped_df.iterrows():
    accumulated_roi = accumulated_roi * (1 + row['performance'])
    roi_total.append(accumulated_roi)

grouped_df['return_total'] = roi_total

fig_roi = px.line(grouped_df, x='date', y='return_total', markers=True, labels={'performance': 'Mean Performance', 'date': 'Date'})
fig_roi.update_traces(line_color='orange')
fig_roi.add_trace(
    go.Scatter(
        x=[df_filtrado['date'].min(), df_filtrado['date'].max()],
        y=[1000, 1000],
        mode='lines',
        name='Initial Investment',
        line=dict(color="black", width=2, dash="dash"),
    )
)

st.markdown("##### Return on investment of 1000 dollars")
st.plotly_chart(fig_roi)

grouped_df_performance = df_filtrado.groupby('date')['performance'].mean().reset_index()
fig_performance = px.line(grouped_df_performance, x='date', y='performance', markers=True,
                          labels={'performance': 'Mean Performance', 'date': 'Date'})
fig_performance.update_traces(line_color='green')

st.markdown("##### Mean performance")
st.plotly_chart(fig_performance)
