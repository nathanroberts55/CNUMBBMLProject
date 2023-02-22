#!/usr/local/bin/python
import numpy as np
import pandas as pd
import re
from scrape_data import scrape_data 
from save_data import send_data

#---- SCRAPE DATA TO DISK ----
scrape_data()

#---- LOG MESSAGE
print('STARTING DATA CLEANING...')

#---- GLOBAL VARIABLES USED LATER ----
dtypes = {
'off'       : 'int8',
'def'       : 'int8',
'tot'       : 'int8',
'pf'        : 'int8',
'ast'       : 'int8',
't/o'       : 'int8',
'blk'       : 'int8',
'stl'       : 'int8',
'fgm'       : 'int8',
'fga'       : 'int8',
'3fgm'      : 'int8',
'3fga'      : 'int8',
'ftm'       : 'int8',
'fta'       : 'int8',
'opp_off'   : 'int8',
'opp_def'   : 'int8',
'opp_tot'   : 'int8',
'opp_pf'    : 'int8',
'opp_ast'   : 'int8',
'opp_t/o'   : 'int8',
'opp_blk'   : 'int8',
'opp_stl'   : 'int8',
'opp_fgm'   : 'int8',
'opp_fga'   : 'int8',
'opp_3fgm'  : 'int8',
'opp_3fga'  : 'int8',
'opp_ftm'   : 'int8',
'opp_fta'   : 'int8',
'rb avg'    : 'float16',
'fg%'       : 'float16',
'3pt%'      : 'float16',
'ft%'       : 'float16',
'opp_rb avg': 'float16',
'opp_fg%'   : 'float16',
'opp_3pt%'  : 'float16',
'opp_ft%'   : 'float16',
'cnu_score' : 'int8',
'opp_score' : 'int8'
}

# Some Team names are inconsistent/duplicated, this dictionary contains those names and the value I want to change them to.
duplicates = {
 'FROSTBURG'                   : 'FROSTBURG STATE UNIVERSITY',
 'FROSTBURG STATE'             : 'FROSTBURG STATE UNIVERSITY',
 'GREENSBORO'                  : 'GREENSBORO COLLEGE',
 'GREENSBORO COLLEGE'          : 'GREENSBORO COLLEGE',
 'KEENE STATE'                 : 'KEENE STATE COLLEGE',
 'KEENE STATE COLLEGE'         : 'KEENE STATE COLLEGE',
 'LAGRANGE'                    : 'LAGRANGE COLLEGE',
 'LAGRANGE COLLEGE'            : 'LAGRANGE COLLEGE',
 'LYNCHBURG'                   : 'LYNCHBURG UNIVERSITY',
 'LYNCHBURG COLLEGE'           : 'LYNCHBURG UNIVERSITY',
 'MARYMOUNT'                   : 'MARYMOUNT (VA.)',
 'MARYMOUNT (VA)'              : 'MARYMOUNT (VA.)',
 'MARYMOUNT (VA.)'             : 'MARYMOUNT (VA.)',
 'MARYVILLE'                   : 'MARYVILLE COLLEGE',
 'MARYVILLE COLLEGE SCOTS'     : 'MARYVILLE COLLEGE',
 'PENN ST. HARRISBURG'         : 'PENN STATE HARRISBURG',
 'PENN ST.-HARRISBURG'         : 'PENN STATE HARRISBURG',
 'PENN STATE HARRISBUR'        : 'PENN STATE HARRISBURG',
 'PENN STATE HARRISBURG'       : 'PENN STATE HARRISBURG',
 'SHENANDOAH'                  : 'SHENANDOAH UNIVERSITY',
 'SHENANDOAH HORNETS'          : 'SHENANDOAH UNIVERSITY',
 'SOUTHERN VA.'                : 'SOUTHERN VIRGINIA UNIVERSITY',
 'SOUTHERN VIRGINIA'           : 'SOUTHERN VIRGINIA UNIVERSITY',
 'SOUTHERN VIRGINIA UNIVERSITY': 'SOUTHERN VIRGINIA UNIVERSITY',
 "ST. MARY'S (MD)"             : "ST. MARY'S (MD.)",
 "ST. MARY'S (MD.)"            : "ST. MARY'S (MD.)",
 'VA. WESLEYAN'                : 'VIRGINIA WESLEYAN UNIVERSITY',
 'VIRGINIA WESLEYAN'           : 'VIRGINIA WESLEYAN UNIVERSITY',
 'WASH. & LEE'                 : 'WASHINGTON AND LEE UNIVERSITY',
 'WASHINGTON & LEE'            : 'WASHINGTON AND LEE UNIVERSITY',
 'WASHINGTON AND LEE'          : 'WASHINGTON AND LEE UNIVERSITY',
 'WASHINGTON COL.'             : 'WASHINGTON COLLEGE',
 'WASHINGTON COLLEGE'          : 'WASHINGTON COLLEGE',
 'WIS.-STEVENS POINT'          : 'WISC.-STEVENS POINT',
 'WISC.-STEVENS POINT'         : 'WISC.-STEVENS POINT',
 'YORK (N.Y.)'                 : 'YORK (N.Y.)',
 'YORK (NY)'                   : 'YORK (N.Y.)'
}

#---- DATA CLEANING/FEATURE ENGINEERING FUNCTIONS ----
def split_columns(df, cols):
  
  # Function  will take the df and split the column name into two new columns for the dataframe
  for col in cols:
    new_cols = col.split('-')
    # Then will go through the original column and split the data in the column on it's seperator
    df[[new_cols[0], new_cols[1]]] = df[col].str.split('-', expand=True)
    # Drop the orginal column to remove the repetitive data
    df.drop(col, axis=1, inplace=True) 
    
# Create Home vs Away Column
def home_court(df):
    df['home'] = [0 if x[:2] == 'at' else 1 for x in df['opponent']]

def extract_date(df):
    # Convert column to year
    df['date'] = pd.to_datetime(df['date'])
    
    # Extract the month, day, year and weekday and make them their own columns
    df['month']   = df['date'].dt.month
    df['day']     = df['date'].dt.day
    df['year']    = df['date'].dt.year
    df['weekday'] = df['date'].dt.weekday

# Clean the Opponent Column
def clean_teamName(df):
  # Create a Ranked Column: if team name contains a ranking value is 1, else 0.
  ranked_mapping = {True: 1, False: 0}
  ranking = df.opponent.str.contains(r'\#\d+', regex=True, case=False, na=False)
  df['ranked'] = ranking.map(ranked_mapping)
  # Remove the numbers/rankings
  df['opponent'] = df['opponent'].str.replace('\#\d+', '', regex=True)
  # Remove the 'at' denoting away games
  df['opponent'] = df['opponent'].apply(lambda x: x[2:] if x[:2] == 'at' else x)
  # Remove the 'vs' denoting neutral location games
  df['opponent'] = df['opponent'].apply(lambda x: x[2:] if x[:2] == 'vs' else x)
   # Capitalize the Team Name
  df['opponent'] = df['opponent'].apply(lambda x: x.upper())
  # Remove Leading White Space
  df['opponent'] = df['opponent'].apply(lambda x: x.lstrip())
  
def clean_win(df):
    df['overtime'] = [1 if x[1:] == 'ot' else 0 for x in df['w/l']]
    df['win'] = [1 if x[:1] == 'W' else 0 for x in df['w/l']]

# Differentials are just the difference between CNU minus the other Teams value in a certain statistical category
# The value will be postive is CNU had a higher count than the other team, negative for the inverse.
def differentials(df):
    df['off_diff']  = df['off'] - df['opp_off']
    df['def_diff']  = df['def'] - df['opp_def']
    df['tot_diff']  = df['tot'] - df['opp_tot']
    df['pf_diff']   = df['pf'] - df['opp_pf']
    df['ast_diff']  = df['ast'] - df['opp_ast']
    df['t/o_diff']  = df['t/o'] - df['opp_t/o']
    df['blk_diff']  = df['blk'] - df['opp_blk']
    df['stl_diff']  = df['stl'] - df['opp_stl']
    df['fgm_diff']  = df['fgm'] - df['opp_fgm']
    df['fga_diff']  = df['fga'] - df['opp_fga']
    df['3fgm_diff'] = df['3fgm'] - df['opp_3fgm']
    df['3fga_diff'] = df['3fga'] - df['opp_3fga']
    df['ftm_diff']  = df['ftm'] - df['opp_ftm']
    df['fta_diff']  = df['fta'] - df['opp_fta']
    df['fg%_diff']  = df['fg%'] - df['opp_fg%']
    df['3pt%_diff'] = df['3pt%'] - df['opp_3pt%']
    df['ft%_diff']  = df['ft%'] - df['opp_ft%']

#---- DATA CLEANING ----
# Import data to dataframes
raw_cnu = pd.read_csv('output/csv/cnuStats.csv')
raw_opp = pd.read_csv('output/csv/oppStats.csv')

# Rename Columns
rename_columns = {
    'Score'  : 'cnu_score-opp_score',
    '3fg-fga': '3fgm-3fga',
    'pct'    : 'fg%',
    'pct.1'  : '3pt%',
    'pct.2'  : 'ft%',
    'avg'    : 'rb avg',
    'avg.1'  : 'ppg avg'}
raw_cnu = raw_cnu.rename(columns=rename_columns)
raw_opp = raw_opp.rename(columns=rename_columns)

# Split Columns
cols_to_split = ['cnu_score-opp_score','fgm-fga', '3fgm-3fga', 'ftm-fta']

split_columns(raw_cnu, cols_to_split)
split_columns(raw_opp, cols_to_split)

# Lowercase column names
raw_cnu.columns = raw_cnu.columns.str.lower()
raw_opp.columns = raw_opp.columns.str.lower()

# Prepend 'opp_' to opp name columns 
opp_cols = ['fg%', '3pt%', 'ft%', 'off', 'def', 'tot', 'rb avg', 'pf', 'ast', 't/o', 'blk', 'stl', 'pts', 'ppg avg', 'fgm', 'fga', '3fgm', '3fga', 'ftm', 'fta', 'ranked']
raw_opp = raw_opp.rename(columns={col:f'opp_{col}' for col in opp_cols})

#-- Feature Engineering--
# Create homecourt advantage column
home_court(raw_cnu)
home_court(raw_opp)

# Create columns for month, day, year, and weekday
extract_date(raw_cnu)

# Perform data cleaning on opponent column
clean_teamName(raw_cnu)
clean_teamName(raw_opp)

# Create a win and overtime column then drop the orignial win/loss column
clean_win(raw_cnu)
clean_win(raw_opp)
raw_cnu = raw_cnu.drop(['w/l'], axis=1)
raw_opp = raw_opp.drop(['w/l'], axis=1)

# Create list of shared columns to be used to merge the dataframes (without the date)
combine_cols = [x for x in list(raw_cnu.columns) if x in list(raw_opp.columns)]
combine_cols.remove('date')

# Merge the columns and drop the duplicate date columns
combined_df = raw_cnu.merge(raw_opp, on=combine_cols)
combined_df = combined_df.drop(['date_y'], axis=1).rename(columns={'date_x':'date'})

# Assign the dtypes for numeric columns for differential calculations
combined_df = combined_df.astype(dtype=dtypes)

# Create differentials for the numeric stats
differentials(combined_df)

# Replace Duplicate names in the opponents columns
combined_df.opponent = combined_df.opponent.replace(duplicates)

# Sort the columns 
combined_df = combined_df.reindex(sorted(combined_df.columns), axis=1)

combined_df.to_csv('output/csv/cleaned_data.csv', index=False)

send_data()
#---- LOG MESSAGE
print('DATA CLEANING COMPLETE...')