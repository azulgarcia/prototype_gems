### Descripción de la app: 
Muestra la performance de la cantidad de proyectos seleccionados de la plataforma polygon
- Se obtienen por semana, los 100 mejores proyectos de polygon de la api de coingecko, y se ordenan por score del top general. 
- La performance se obtiene, de manera dinámica, como la media de las performances semanales de la cantidad de proyectos seleccionados en la app.
- Se puede ver el test de 1000usd para los proyectos seleccionados, también calculado de manera dinámica.
- Se muestra una tabla con los proyectos considerados por semana y su performance.
- Se muestra otra tabla con los proyectos de la semana actual, con su precio de inicio.

### Actualización:
- Ejecutar el script update_prices_last_week.py, que toma los proyectos de la semana anterior y calcula su precios finales y performances. Los resultados se debe agregar al archivo modification_polygon_coningecko.csv.
- Ejecutar el script update_polygon_current_week.py que busca los proyectos de la semana actual con su precio de inicio. Los resultados deben reemplazar a los del archivo polygon_coingecko_current.csv. Siempre, hay que agregar Bitcoin con el precio de la semana actual a este listado.
- Ejecutar el script update_new_project_hist.py, que obtiene el historico de precios y performances de nuevos proyectos que aparecen en el top 100 de coingecko actual y no habían aparecido antes. 

