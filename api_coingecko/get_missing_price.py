import pandas as pd
from cb_database_queries import (get_top_projects_scores,
                                 get_top_projects_price,
                                 get_projects_slug,)
from app_polygon.update.cb_database_connection import open_connection, close_connection
from datetime import date
import time
import requests
import json
# ============================================================================
# The script generate a csv with all projects from the TOP that contains
# missing prices in mysql database
# get the missing id_projects, obtain the slug, do a request to coingecko
# create a dataframe with
# 'id_project','price','created_at']
# ============================================================================
TIME_SLEEP = 10


def obtain_missing_prices(connection,
                          category,
                          top_position,
                          year,
                          initial_week,
                          final_week):
    """
    Find projects with missing price on mysql data base.

    Find missing price from mysql where projects in the top
    and their prices from week and week + 1 are missing.

    Args:
        - connection (_type_): to data-base
        - category (_type_): project category
        - top_position (_type_): max position
        - year (_type_): year to calculate query
        final_week (_type_): final week

    Returns:
        pandas data frame of missing price:
        price, date

    """
    top_projects_scores = get_top_projects_scores(connection,
                                                  top_position + 1,
                                                  category,
                                                  year,
                                                  initial_week,
                                                  final_week)
    week = initial_week
    columns = ['id_project', 'price', 'created_at']
    data = []
    while week <= final_week:
        print('week:', week, category)
        if 'week' in top_projects_scores.columns:
            for project in top_projects_scores[top_projects_scores['week'] == week]['id_project']:
                project_init_week = get_top_projects_price(connection,
                                                           project,
                                                           year,
                                                           week)
                if week < 52:
                    project_end_week = get_top_projects_price(connection,
                                                              project,
                                                              year,
                                                              week + 1)
                if week == 52:
                    project_end_week = get_top_projects_price(connection,
                                                              project,
                                                              year + 1,
                                                              1)

                if project_init_week.empty:
                    slug = get_projects_slug(connection, project)
                    iso_date = date.fromisocalendar(year, week, 6)
                    coingecko_date = weeknum_to_dates(iso_date)
                    price = get_price_from_coingecko(slug, coingecko_date)
                    time.sleep(TIME_SLEEP)
                    if price is None:
                        print('No price:', project, 'week', week, category)
                    else:
                        print(project, price, iso_date)
                        data.append({
                                    'id_project': project,
                                    'price': price,
                                    'created_at': iso_date,
                                    })
                if project_end_week.empty:
                    slug = get_projects_slug(connection, project)
                    iso_date = date.fromisocalendar(year, week + 1, 6)
                    coingecko_date = weeknum_to_dates(iso_date)
                    price = get_price_from_coingecko(slug, coingecko_date)
                    time.sleep(TIME_SLEEP)
                    if price is None:
                        print('No price:', project, 'week', week + 1, category)
                    else:
                        print(project, price, iso_date)
                        data.append({
                                    'id_project': project,
                                    'price': price,
                                    'created_at': iso_date,
                                    })
        week += 1
    return pd.DataFrame(columns=columns, data=data)


def get_price_from_coingecko(slug, date):
    url = f'https://api.coingecko.com/api/v3/coins/{slug}/history?date={date}localization=false'
    print(url)
    response_api = requests.get(url)
    data = response_api.text
    parse_json = json.loads(data)
    try:
        price = parse_json['market_data']['current_price']['usd']
        return price
    except:
        print(f'Error coingecko at project {slug}, {date}')


def weeknum_to_dates(iso_date):
    """
    Week number conversion
    convert from 2022-01-28 to 28-01-2022
    coingecko needs on this format"""
    missing_date = str(iso_date)
    date_ = missing_date.split('-')
    return f'{date_[2]}-{date_[1]}-{date_[0]}'


if __name__ == '__main__':
    # ========================================================================
    # The script generate a csv with all projects from the TOP that
    # contains missing prices in mysql database
    # get the missing id_projects, obtain the slug, do a request to coingecko
    # create a dataframe with
    # 'id_project','price','created_at']
    # =========================================================================
    connection = open_connection()
    TOP_POSITION = 10
    YEAR = 2024
    INITIAL_WEEK = 7
    FINAL_WEEK = 7

    categories = ['General',
                  'Development',
                  'Reddit',
                  'Gems',
                  '4Chan',
                  'DeFi',
                  'Metaverse',
                  'BSC'
                  ]
    missing_price = pd.DataFrame()
    for category in categories:
        missing_price = pd.concat([
            missing_price,
            obtain_missing_prices(connection,
                                  category,
                                  TOP_POSITION,
                                  YEAR,
                                  INITIAL_WEEK,
                                  FINAL_WEEK)
                                  ],
            ignore_index=True, )
    missing_price.drop_duplicates(inplace=True)
    missing_price.to_csv('updater_script/data/missing_prices.csv',
                         sep=',',
                         index=False)
    close_connection(connection)
