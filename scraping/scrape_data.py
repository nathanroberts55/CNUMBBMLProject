#!/usr/bin/python
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

#---- CONSTANTS ----
END_CURRENT_SEASON = datetime.now().year + 1 if datetime.now().month > 10 else datetime.now().year
YEARS = [x for x in range(2010,END_CURRENT_SEASON) if x not in [2020]]
TEAM_STATS_URL = "https://static.cnusports.com/custompages/mbball/Stats/{}/teamgbg.htm"
DIR_LIST = ['output', 'output/html', 'output/csv', 'output/processed_data', 'output/models', 'output/joblib']

#---- FUNCTION TO GET DATA ----
def scrape_data():
    # Log Message
    print('STARTING DATA SCRAPE....')
    
    #---- CREATE FILE STRUCTURE ----
    for dir in DIR_LIST:
        if not os.path.exists(dir):
            os.makedirs(dir)
            print(f'Created Path at: {dir}')
        else:
            print(f'Directory at {dir} already exists, skipping...')
            
    # TODO: Update to only scrape the current season if the other seasons already exists
     
    #---- SCRAPE WEB PAGES, SAVE TO DISK ----
    for year in YEARS:
        url = TEAM_STATS_URL.format(f"{year}-{year + 1}")
        data = requests.get(url)
        
        with open(f"{DIR_LIST[1]}/{year}-{year + 1}.html", "w+") as f:
            f.write(data.text)
        
    #---- TURN DATA INTO DATAFRAMES FOR PROCESSING ----
    # Lists for each season dataframe
    cnu_dfs = []
    opp_dfs = []

    for year in YEARS:
        # Read the HTML from the pages we have saved
        with open(f"{DIR_LIST[1]}/{year}-{year + 1}.html") as f:
            page = f.read()
    
        # Initialize the parser
        soup = BeautifulSoup(page, "html.parser")
        
        # Get the data from the first (CNU) Table
        try:
            cnu_table = soup.findAll('table')[1]
            print(f"CNU Team Data Collected from: {year}-{year + 1}")
        except:
            print("Less than one cnu table available")
            
        # Get the data from the second (Opp) Table
        try:
            opp_table = soup.findAll('table')[4]
            print(f"Opponent Team Data Collected from: {year}-{year + 1}")
        except:
            print("Less than one opp table available")
        
        #Remove the Summary Table that is at the bottom of CNU Table
        try:
            summary_table = cnu_table.findAll('table')[0]
            summary_table.decompose()
        except:
            print("No Nested Summary Table")
            continue
        
        #Remove the Summary Table that is at the bottom of Opp Table
        try:
            summary_table = opp_table.findAll('table')[0]
            summary_table.decompose()
        except:
            print("No Nested Summary Table")
            continue
    
        # Remove the grouping info row from CNU Table
        info_row = cnu_table.find('tr')
        info_row.decompose()
        
        # Remove the grouping info row from CNU Table
        info_row = opp_table.find('tr')
        info_row.decompose()
        
        # Remove the Total Calculation Rows at the bottom
        cnu_selected_rows = cnu_table.findAll('tr')[-5:]
        opp_selected_rows = opp_table.findAll('tr')[-5:]
        for row in cnu_selected_rows:
            row.decompose()
        for row in opp_selected_rows:
            row.decompose()
            
        # Read Data into CNU Dataframe
        df = pd.read_html(str(cnu_table))[0]
        df.columns = df.iloc[0] 
        df = df[1:]
        df["Season"] = f'{year}-{year + 1}'
        cnu_dfs.append(df)
        
        # Read Data into Opp Dataframe
        df = pd.read_html(str(opp_table))[0]
        df.columns = df.iloc[0] 
        df = df[1:]
        df["Season"] = f'{year}-{year + 1}'
        opp_dfs.append(df)
    
    #---- COMBINE DATA FRAMES INTO ONE ----
    cnu_stats = pd.concat(cnu_dfs)
    opp_stats = pd.concat(opp_dfs)

    #---- RESET INDICES ----
    cnu_stats.reset_index(drop=True, inplace=True)
    opp_stats.reset_index(drop=True, inplace=True)

    #---- SAVE DATAFRAMES TO CSV
    cnu_stats.to_csv(f"{DIR_LIST[2]}/cnuStats.csv", index=False)
    opp_stats.to_csv(f"{DIR_LIST[2]}/oppStats.csv", index=False)
    
    # Log Message
    print('DATA SCRAPE COMPLETE...')