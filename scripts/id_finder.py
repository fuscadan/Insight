"""
Created on Mon September  16 2019

@author: danie

    This program creates a list of ESPN NBA game ID numbers by visiting each
    team's schedule page for each year in the selected range and scraping the 
    IDs for home games (to avoid double-counting).  Game IDs may be found for
    either the regular season or the postseason. 
    
    The ID numbers are saved to a file: 
        "espn_game_ids_(season type)_(start year)-(end year).txt"
"""

import urllib3
from bs4 import BeautifulSoup

# parameters for the scope of the scrape
START_YEAR = 2017
END_YEAR = 2018
SEASON_TYPE = 2     #see SEASON_TYPE_NAMES below

# static elements of the urls that are to be looked up. Typical format:
# http://www.espn.com/nba/team/schedule/_/name/wsh/season/2016/seasontype/2
SCHEDULE_ROOT = 'http://www.espn.com/nba/team/schedule/_/name/'
TEAM_ABBREVIATIONS = ['atl', 'bos', 'bkn', 'cle', 'cha', 'chi', 'dal', 'den', 
    'det', 'gs', 'hou', 'ind', 'lac', 'lal', 'mem', 'mia', 'mil', 'min', 'no', 
    'ny', 'okc', 'orl', 'phi', 'phx', 'por', 'sac', 'sa', 'tor', 'utah', 'wsh']
SEASON_TYPE_NAMES = {1 : 'preseason', 2 : 'regular_season' , 3 : 'postseason'} 

# file path strings
RELATIVE_PATH = 'Git/data/'
ID_FILE_PATH = (RELATIVE_PATH
    + 'raw/' 
    + 'espn_game_ids_{0}_{1}-{2}.txt'.format(
        SEASON_TYPE_NAMES[SEASON_TYPE],str(START_YEAR),str(END_YEAR)
        )
    )

if __name__ == '__main__':
    # Find ESPN game IDs from the webpages displaying the season schedule of
    # each team.  Print basic information while looping to monitor progress.
    http = urllib3.PoolManager()

    with open(ID_FILE_PATH, 'w') as id_file:
        for year in range(START_YEAR, END_YEAR + 1):
            print(year)
            
            for team in TEAM_ABBREVIATIONS:
                print(team)

                url = (SCHEDULE_ROOT 
                    + team 
                    + '/season/' 
                    + str(year) 
                    + '/seasontype/' 
                    + str(SEASON_TYPE)
                    ) 
                r = http.request('GET', url)
                soup = BeautifulSoup(r.data, 'html.parser')
                
                n_games_in_season = len(soup.select('.ml4 a'))
                
                for i in range(n_games_in_season):
                    if i == 20:
                        print(i)
                    elif i == 40:
                        print(i)
                    elif i == 60:
                        print(i)
                    elif i == 80:
                        print(i)

                    # find the tag with the href link to the i^th game and grab
                    # the game ID as an integer
                    game_link_tag = soup.select('.ml4 a')[i]
                    game_id = game_link_tag.get('href')[-9:]

                    # find the tag with the "vs" or "@" string (indicating 
                    # whether the game was at home or not) and grab that string
                    location_tag = game_link_tag.parent.parent.previous_sibling
                    game_location = location_tag.select('.pr2')[0].text
                    
                    # Only write game IDs of home games, to avoid double-
                    # counting when the schedules of every team are scraped.
                    if game_location == 'vs':
                        id_file.write(game_id + '\n')
                        
    
    
