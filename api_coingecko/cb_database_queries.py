import pandas as pd
from pyparsing import Any


def get_top_projects_scores(
                            connection,
                            top_position,
                            category,
                            year,
                            init_week,
                            end_week):
    """
    - Gets a query to obtain top projects from an especific category.

        Args:
        - connection: connection to de DB.

        Returns:
        - project_score from the top_position (ideally top 10).
    """
    try:
        cursor = connection.cursor(dictionary=True)
        #sql_select_query = 'SELECT id_project,week,top,score,position,DATE(created_at) as created_at,YEAR(created_at) as year FROM projects_scores where position>0 and position<%s and top = %s and YEAR(created_at) = %s and week BETWEEN %s AND %s;'
        sql_select_query = 'SELECT id_project, projects.name, week, projects_scores.top, score, position, DATE(projects_scores.created_at) as created_at,YEAR(projects_scores.created_at) as year FROM projects_scores inner join  projects on projects_scores.id_project = projects.id where position>0 and position<%s and top = %s and YEAR(projects_scores.created_at) = %s and week BETWEEN %s AND %s+1;'
        cursor.execute(sql_select_query, (
                                        top_position,
                                        category,
                                        year,
                                        init_week,
                                        end_week,))
        result = cursor.fetchall()
        all_pojects = pd.DataFrame(result)

        return all_pojects
    finally:
        cursor.close()


def get_top_projects_price(
                            connection: Any,
                            id_project: Any,
                            year: Any,
                            week: Any) -> pd.DataFrame:

    """Gets a query to obtain prices from an especific category.

    @param connection: connection to de DB
    @param id_project: project
    @param week:
    @return price data frame from the ide_project in year and week
    """
    try:
        cursor = connection.cursor(dictionary=True)
        sql_select_query = 'select id_project, price, DATE(created_at) as created_at, week(created_at) as week,YEAR(created_at) as year from prices where id_project= %s and YEAR(created_at) = %s and week(created_at) = %s;'
        cursor.execute(sql_select_query, (id_project, year, week,))
        result = cursor.fetchall()
        all_contest = pd.DataFrame(result)
        return all_contest
    finally:
        cursor.close()


def get_projects_name(connection):

    '''
    return a data frame with the name of all projects from the data base,
    '''    
    try:
        cursor = connection.cursor(dictionary=True)
        sql_query = ('SELECT id as id_project, slug, name, ticker,marketcap, volume FROM projects Where slug is not null and name is not null')        
        cursor.execute(sql_query)
        data_names = cursor.fetchall()
        return pd.DataFrame(data_names)
    finally:
        cursor.close()

def get_projects_slug(connection, id_project):

    '''
    return slug based on id_project
    '''
    try:
        cursor = connection.cursor(dictionary=True)
        sql_query = ('SELECT slug FROM projects WHERE id = %s')
        cursor.execute(sql_query, (id_project,))
        data_slug = cursor.fetchall()
        #print(data_slug)
        return data_slug[0]['slug']
    finally:
        cursor.close()


"""

def performance_per(x1,x2):
    return round(100.0*(x2-x1)/x1,2)

def projects_performance(connection, dataframe_projects,id_contest):
    '''
    @param connetion: connector to the DB
    @param project_id: is the top 10 or top25 or topN that we wan to analize the historical
    @param id_contest: is the contest where we want to obtain the performance of project
    @return a performance float 0-100%'''

    rend = [one_project_performance(connection,i,id_contest) for i in dataframe_projects['id_project']]
    #print(rend)

    dataframe_projects['performance'] = rend
    return dataframe_projects
"""

"""
if __name__ == '__main__':
    #from bisect import bisect
    #from cb_loadData import getContestData, load_json
    #from cb_processingData import adding_name, points_per_slug_calculator, info_current_contest,best_topN_project    
    from cb_database_connection import open_connection, close_connection
    from dash import Dash, html, dcc, Input, Output
    import plotly.express as px        
    connection = open_connection()
    id_project = 4688
    slug = get_projects_slug(connection,id_project)
    print(slug)
    close_connection(connection)

    top_position = 10
    category = 'General'
    init_week = 5
    end_week = 10
    year = 2022
    general_projects = get_top_projects_scores(connection,top_position,category,year,init_week,end_week)    
    print(general_projects)
    id_project = 376
    year = 2022
    week = 1
    project_price =get_top_projects_price(connection,id_project,year,week)
    print(project_price)
    close_connection(connection)"""