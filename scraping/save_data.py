#!/usr/bin/python
import os
import requests
import pandas as pd
import json

def row_to_json(row):
    json = {
        "three_fga":  row['3fga'],
        "three_fga_diff": row['3fga_diff'],
        "three_fgm": row['3fgm'],
        "three_fgm_diff": row['3fgm_diff'],
        "three_pt_percent": row['3pt%'],
        "three_pt_percent_diff": row['3pt%_diff'],
        "ast": row['ast'],
        "ast_diff":  row['ast_diff'],
        "blk": row['blk'],
        "blk_diff": row['blk_diff'],
        "cnu_score": row['cnu_score'],
        "date": row['date'],
        "day": row['day'],
        "def_reb": row['def'],
        "def_diff": row['def_diff'],
        "fg_percent": row['fg%'],
        "fg_percent_diff": row['fg%_diff'],
        "fga":  row['fga'],
        "fga_diff": row['fga_diff'],
        "fgm": row['fgm'],
        "fgm_diff": row['fgm_diff'],
        "ft_percent": row['ft%'],
        "ft_percent_diff": row['ft%_diff'],
        "fta": row['fta'],
        "fta_diff": row['fta_diff'],
        "ftm": row['ftm'],
        "ftm_diff": row['ftm_diff'],
        "home": row['home'],
        "month": row['month'],
        "off_reb": row['off'],
        "off_diff": row['off_diff'],
        "opp_three_fga": row['opp_3fga'],
        "opp_three_fgm": row['opp_3fgm'],
        "opp_three_pt_percent": row['opp_3pt%'],
        "opp_ast": row['opp_ast'],
        "opp_blk": row['opp_blk'],
        "opp_def": row['opp_def'],
        "opp_fg_percent": row['opp_fg%'],
        "opp_fga": row['opp_fga'],
        "opp_fgm": row['opp_fgm'],
        "opp_ft_percent": row['opp_ft%'],
        "opp_fta": row['opp_fta'],
        "opp_ftm": row['opp_ftm'],
        "opp_off_reb": row['opp_off'],
        "opp_pf": row['opp_pf'],
        "opp_ppg_avg": row['opp_ppg avg'],
        "opp_pts": row['opp_pts'],
        "opp_rb_avg": row['opp_rb avg'],
        "opp_score": row['opp_score'],
        "opp_stl": row['opp_stl'],
        "opp_turnover": row['opp_t/o'],
        "opp_tot_reb": row['opp_tot'],
        "opponent": row['opponent'],
        "overtime": row['overtime'],
        "pf": row['pf'],
        "pf_diff": row['pf_diff'],
        "ppg_avg": row['ppg avg'],
        "pts": row['pts'],
        "ranked": row['ranked'],
        "rb_avg": row['rb avg'],
        "season": row['season'],
        "stl": row['stl'],
        "stl_diff": row['stl_diff'],
        "turnover": row['t/o'],
        "turnover_diff": row['t/o_diff'],
        "tot_reb": row['tot'],
        "tot_diff": row['tot_diff'],
        "weekday": row['weekday'],
        "win": row['win'],
        "year": row['year']
    }
     
    return json
    
def send_data():
    URL = 'http://api/gamestats'
    HEADERS = {"accept": "application/json", "Content-Type": "application/json"}
    
    print('SENDING DATA TO DATABASE...')
    
    clean_data = pd.read_csv('output/csv/cleaned_data.csv')
    clean_data.reset_index()
    
    for index, row in clean_data.iterrows():
        payload = row_to_json(row)
        res = requests.post(url=URL, headers=HEADERS, json=payload)
        print(res.text)
    
    print('DATA SENT TO DATABASE... ')
    
def main():
    send_data()
    
if __name__ == "__main__":
     main()
     
    


 
 
 
 
 
 
