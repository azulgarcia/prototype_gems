import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


df = pd.read_csv('all_categories_performance.csv')
df['date'] = pd.to_datetime(df['date'])

###############################################################################################################
# Performance for date
###############################################################################################################
#grouped_df = df.groupby(['category', 'date']).agg({'performance': 'sum'}).reset_index()

category_filter = ['Gems', 'Gems<15', 'Gems<25']
filtered_df = df[df['category'].isin(category_filter)]

year_filter = [2023, 2024]
filtered_df = filtered_df[filtered_df['date'].dt.year.isin(year_filter)]
filtered_df['date'] = pd.to_datetime(filtered_df['date']).dt.date

print(filtered_df.columns)

###############################################################################################################
# All projects for year and week
###############################################################################################################
all_gems_df = df[df['category'].isin(category_filter)]
all_gems_df = all_gems_df[all_gems_df['date'].dt.year.isin(year_filter)]
print(all_gems_df)

###############################################################################################################
# Streamlit app
###############################################################################################################

st.title('Performance Gems')

rango_fechas = pd.date_range(df['date'].min(), df['date'].max())
fecha_inicio_default = max(rango_fechas.min().date(), filtered_df['date'].min())  # Establecer un valor predeterminado dentro del rango
fecha_fin_default = min(rango_fechas.max().date(), filtered_df['date'].max())  # Establecer un valor predeterminado dentro del rango
fecha_inicio = st.date_input("Select start date",
                             min_value=rango_fechas.min().date(),
                             max_value=rango_fechas.max().date(),
                             value=fecha_inicio_default)
fecha_fin = st.date_input("Select end date",
                          min_value=rango_fechas.min().date(),
                          max_value=rango_fechas.max().date(),
                          value=fecha_fin_default)

df_filtrado = filtered_df[(filtered_df['date'] >= fecha_inicio) & (filtered_df['date'] <= fecha_fin)]

df_filtrado = df_filtrado.groupby(['category', 'date'])['performance'].mean().reset_index()

init_investment = 1000
roi_total = []

for category in df_filtrado['category'].unique():
    category_df = df_filtrado[df_filtrado['category'] == category]
    accumulated_roi = init_investment
    for index, row in category_df.iterrows():
        accumulated_roi *= 1 + row['performance']
        roi_total.append(accumulated_roi)

df_filtrado['return_total'] = roi_total

fig_roi = px.line(df_filtrado, x='date', y='return_total', color='category', markers=True,
                  labels={'performance': 'Mean Performance', 'date': 'Date'},)


fig_roi.add_trace(
    go.Scatter(
        x=[df_filtrado['date'].min(), df_filtrado['date'].max()],
        y=[1000, 1000],
        mode='lines',
        name='Initial Investment',
        line=dict(color="black", width=2, dash="dash"),
    )
)

st.write("Return on investment of 1000 dollars")
st.plotly_chart(fig_roi)

st.title('Projects by category and date')
categorias = all_gems_df['category'].unique()
categoria_seleccionada = st.selectbox('Select category', categorias)

years = all_gems_df['year'].unique()
year_seleccionado = st.selectbox('Select year', years)

semanas = all_gems_df[all_gems_df['year'] == year_seleccionado]['week'].unique()
semana_seleccionada = st.selectbox('Select week', semanas)

filtered_gems = all_gems_df[(all_gems_df['category'] == categoria_seleccionada)
                          & (all_gems_df['year'] == year_seleccionado)
                          & (all_gems_df['week'] == semana_seleccionada)]


columnas_a_mostrar = ['category', 'date', 'project_name', 'start_price', 'end_price', 'performance']

st.write(filtered_gems[columnas_a_mostrar])