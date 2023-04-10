import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="CNU Basketball Data Dashboard",
    page_icon="	:trophy:",
    layout='wide',
    initial_sidebar_state='collapsed'
)

# --- CONSTANTS ---
table_cols = [
'opponent','date','cnu_score','opp_score','ast','fg%','fga','fgm','3fgm','3fga','3pt%','ft%','fta','ftm','def','off','tot','pf','stl','t/o','blk','opp_ast','opp_fgm','opp_fga','opp_fg%','opp_3fgm','opp_3fga','opp_3pt%','opp_ft%','opp_fta','opp_ftm','opp_def','opp_off','opp_tot','opp_pf','opp_stl','opp_t/o','opp_blk','ast_diff','fg%_diff','fga_diff','fgm_diff','3fga_diff','3fgm_diff','3pt%_diff','ft%_diff','fta_diff','ftm_diff','def_diff','off_diff','tot_diff', 'pf_diff','stl_diff','t/o_diff','blk_diff'
]


# ---- DATA IMPORT ----
@st.cache
def get_data():
    df = pd.read_csv('output/csv/cleaned_data.csv')
    return df

data = get_data()

# --- Remove Hamburger Menu | https://docs.streamlit.io/knowledge-base/using-streamlit/how-hide-hamburger-menu-app ---
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header('CNU Data Data Dashboard')
    
    view = st.selectbox(
        'Choose Data View',
        ('Last Game Stats', 'Overall Stats', 'Scouting'),
        key='ViewSelectBox')


# ---- DATA HEADER ----

st.title('CNUMBB Data Dashboard')
st.markdown('Statistics on the defending 2022-2023 Men\'s DIII National Champions')
st.markdown(" --- ")

if view == 'Last Game Stats':
    # ---- LAST GAME KEY STATS PAGE ----
    st.subheader('Last Game Key Stats')

    col1, col2, col3 = st.columns(3)
    last_game = data.sort_values('date', ascending=False).head(1)
    with col1:
        st.markdown(""" Rebound Differential""")
        st.text(int(last_game['tot_diff']))
    with col2:
        st.markdown(""" Turnover Differential""")
        st.text(int(last_game['t/o_diff']))
    with col3:
        st.markdown(""" Last Game Final Score""")
        st.text(f"{int(last_game['cnu_score'])} - {int(last_game['opp_score'])}")
        
    st.markdown(" --- ")

    # ---- DATA VIZ ----
    st.subheader('Previous Game Data Charts')

    num_games = st.number_input('Select Number of Games (up to 20 Games)', value=5, min_value=5, max_value=20)

    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    prev_games = data.sort_values('date', ascending=False).head(int(num_games))

    # TODO: Use num_games in the title of the graphs
    with row1_col1:
        total_rebs_chart = px.bar(prev_games, 
                            y=['tot', 'opp_tot'], 
                            x='opponent',
                            barmode='group', 
                            labels={"variable": "Team"}, 
                            hover_data=['off', 'def','opp_off', 'opp_def'],
                            title=f'Total Rebounds Per Last {num_games} Games')
        total_rebs_chart.update_layout(xaxis_title='Game', 
                                yaxis_title='Total Rebounds')
        
        st.plotly_chart(total_rebs_chart)
        
    with row1_col2:
        total_turnover_chart = px.bar(prev_games, y=['t/o', 'opp_t/o'], 
        x='opponent', 
        barmode='group', 
        labels={"variable": "Team"}, 
        title=f'Total Turnovers Per Last {num_games} Games')
        total_turnover_chart.update_layout(xaxis_title='Game', 
                                        yaxis_title='Total Rebounds')
        
        st.plotly_chart(total_turnover_chart)

    with row2_col1:
        fg_taken, threes_taken = prev_games[['fga','3fga']].sum()
        avg_fg, avg_three = prev_games[['fg%','3pt%']].mean()
        
        total_shots = px.pie(prev_games, 
                            values=[fg_taken,threes_taken], 
                            names=['Field Goals Attempted', 'Threes Attempted'], 
                            hole=0.3, 
                            title=f'Shot Makeup Over Last {num_games} Games')
        total_shots.update_traces(textposition='outside', 
                                textinfo='label+percent')
        
        st.plotly_chart(total_shots)
        
    with row2_col2:
        fg_chart = go.Figure()
        fg_chart.add_trace(
            go.Scatter(x=prev_games['date'], y=prev_games['fg%'],
                    mode='lines',
                    name='CNU FG%')
        )
        fg_chart.add_trace(
            go.Scatter(x=prev_games['date'], y=prev_games['3pt%'],
                    mode='lines',
                    name='CNU 3PT%')
        )
        fg_chart.add_trace(
            go.Scatter(x=prev_games['date'], y=prev_games['opp_fg%'],
                    mode='lines',
                    name='Opponent FG%')
        )
        fg_chart.add_trace(
            go.Scatter(x=prev_games['date'], y=prev_games['opp_3pt%'],
                    mode='lines',
                    name='Opponent 3PT%')
        )

        st.plotly_chart(fg_chart)
    st.markdown(" --- ")

    # ---- GAME DATA ----
    st.subheader('Full Game Data')
    
    st.dataframe(data=data[table_cols].sort_values('date', ascending=False).set_index('opponent'))

if view == 'Scouting':
    st.subheader('Scouting')
    
    # --- TEAM SELECTION ---
    team = st.selectbox(
        'Select a team',
        data.opponent.unique(),
        key='ScoutTeamSelectBox')
    
    team_data = data[data['opponent'] == team]
    team_data['win_label'] = team_data['win'].map({0:'Loss', 1:'Win'})
    
    # --- GRAPH SECTION SPLIT ---
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    
    # --- GRAPH 1 ---
    with row1_col1:
        games_won = team_data.groupby('win_label')['win_label'].count()
        total_wins = px.pie(games_won,
                            values = 'win_label',
                            names=games_won.index,
                            title=f'Win/Loss vs. {team}')
        total_wins.update_traces(textposition='inside', 
                                textinfo='label+percent',
                                rotation=180)
        st.plotly_chart(total_wins)
    
    # --- GRAPH 2 ---
    with row1_col2:
        avg_score = go.Figure()
        avg_score.add_trace(
            go.Box(
                y=team_data['cnu_score'],
                name='CNU Score'
            )
        )
        avg_score.add_trace(
            go.Box(
                y=team_data['opp_score'],
                name=f'{team} Score'
            )
        )
        avg_score.update_layout(title_text=f'Scoring Distribution vs {team}')
        avg_score.update_traces(boxpoints='all')
        st.plotly_chart(avg_score)
        
    # --- GRAPH 3 ---
    with row2_col1:
        rebounds_comp = px.scatter(team_data,
                              x='tot',
                              y='opp_tot',
                              color='win_label',
                              labels={"win_label": "Win/Loss"},
                              marginal_x="histogram",
                              category_orders = {'win_label':['Win', 'Loss']}
                              )
        rebounds_comp.update_layout(xaxis_title="Total Rebounds (CNU)", yaxis_title=f"Total Rebounds ({team})", title_text=f'Total Rebound Comparison vs {team}')
        st.plotly_chart(rebounds_comp)
    
    # --- GRAPH 4 ---  
    with row2_col2:
        turnovers_comp = px.scatter(team_data,
                              x='t/o',
                              y='opp_t/o',
                              color='win_label',
                              labels={"win_label": "Win/Loss"},
                              marginal_x="histogram",
                              category_orders = {'win_label':['Win', 'Loss']}
                              )
        turnovers_comp.update_layout(xaxis_title="Total Turnovers (CNU)", yaxis_title=f"Total Turnovers ({team})", title_text=f'Total Turnovers Comparison vs {team}')
        st.plotly_chart(turnovers_comp)
    
    # --- GAME DATA ---
    st.subheader(f'Full Game Data vs {team}')

    st.dataframe(data=team_data[table_cols].sort_values('date', ascending=False).set_index('opponent'))
    
if view == 'Overall Stats':
    st.subheader("Overall Statistics")
    st.markdown("These statistics are representative of the data collected from the last 12 years of CNU Men's Basketball. During these years the team has been led by Head Coach John Kirkorian.")
    
    # --- OVERALL STATS ---
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    row3_col1, row3_col2 = st.columns(2)
    row4_col1, row4_col2 = st.columns(2)
    # Wins and Loss Counts
    wins, losses = data.win.value_counts()
    
    # Total Win/Loss
    with row1_col1:
        st.markdown(f"<h4 style='text-align: center;'>Overall Record (W/L)</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>{wins}-{losses}</p>", unsafe_allow_html=True)
    # Winning Percentage
    with row1_col2:
        win_percentage = '{:.3f}'.format(wins/(wins+losses))
        st.markdown(f"<h4 style='text-align: center;'>Overall Win Percentage</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>{win_percentage}</p>", unsafe_allow_html=True)
    # Most Wins in a Season
    with row1_col3:
        most_wins = data.groupby('season')['win'].sum('win').max()
        st.markdown(f"<h4 style='text-align: center;'>Most Wins in a Season</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>{most_wins}</p>", unsafe_allow_html=True)

    # Home Record
    with row2_col1:
        home = data[data['home'] == 1].copy()
        home_win, home_loss = home.win.value_counts()

        st.markdown(f"<h4 style='text-align: center;'>Home Record</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>{home_win}-{home_loss}</p>", unsafe_allow_html=True)
    # Away Record
    with row2_col2:
        away = data[data['home'] == 0].copy()
        away_win, away_loss = away.win.value_counts()
        
        st.markdown(f"<h4 style='text-align: center;'>Away Record</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>{away_win}-{away_loss}</p>", unsafe_allow_html=True)
    # Avg. Opp PPG
    with row2_col3:
        ranked = data[data['ranked'] == 1].copy()
        ranked_win, ranked_loss = ranked.win.value_counts()
        
        st.markdown(f"<h4 style='text-align: center;'>Record Against Ranked Opp.</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>{ranked_win}-{ranked_loss}</p>", unsafe_allow_html=True)
    
    # Most Wins in a Season
    with row3_col1:
        wins_by_season = data.groupby('season')[['win']].sum('win').sort_values('win', ascending=True).tail(5)
        wins_line_chart = px.bar(wins_by_season,
                                 x='win',
                                 y=wins_by_season.index,
                                 text_auto=True,
                                 title="Most Wins in a Season")
        st.plotly_chart(wins_line_chart)
    with row3_col2:
        total_wins = px.pie(data, 
                            values=[wins, losses], 
                            names=['Wins', 'Losses'], 
                            hole=0.3, 
                            title=f'Total Wins vs Losses')
        total_wins.update_traces(textposition='outside', 
                                textinfo='label+percent',
                                rotation=65)
        st.plotly_chart(total_wins)
    
    with row4_col1:
        points_dist = px.histogram(data,
                                        x='cnu_score',
                                        text_auto=True,
                                        title="Overall Points Per Game Distribution",
                                        )
        points_dist.update_layout(bargap=0.2)
        st.plotly_chart(points_dist)
    # Win Margin Per Season
    with row4_col2:
        win_margin = data[data['win'] == 1].copy()
        win_margin['win_margin'] = win_margin['cnu_score'] - win_margin['opp_score']
        win_margin = win_margin.groupby('season')[['win_margin']].mean('win_margin')
        win_margin = win_margin.sort_values('win_margin', ascending=True).head(5)
        win_marging_chart = px.bar(win_margin,
               x='win_margin',
               y=win_margin.index,
               title='Highest Average Win Margin by Season',
               text_auto=True)
        st.plotly_chart(win_marging_chart)
        
    # --- CURRENT SEASON OVERALL STATS ---
    st.subheader("Season Statistics")
    st.markdown("Selecting a season from the dropdown below will provide more detailed statistical analysis of the season selected.")
    # Season Selection
    season = st.selectbox(
        'Select a Season',
        data.season.unique(),
        key='OverallSeasonSelectBox')
    
    season_data = data[data['season'] == season].copy()
    season_data['consecutive_wins'] = season_data.win.groupby((season_data.win != season_data.win.shift()).cumsum()).transform('size') * season_data.win
    
    
    row4_col1, row4_col2, row4_col3 = st.columns(3)
    row5_col1, row5_col2, row5_col3 = st.columns(3)
    row6_col1, row6_col2 = st.columns(2)
    
    # Season Record
    with row4_col1:
        season_wins, season_losses = season_data.win.value_counts()
        st.markdown(f"<h4 style='text-align: center;'>Season Record (W/L)</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>{season_wins}-{season_losses}</p>", unsafe_allow_html=True)
    # Season Win Percentage
    with row4_col2:
        win_percentage = '{:.3f}'.format(season_wins/(season_wins+season_losses))
        st.markdown(f"<h4 style='text-align: center;'>Season Win Percentage</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>{win_percentage}</p>", unsafe_allow_html=True)
    # Longest Win Streak
    with row4_col3:
        longest_win_streak = season_data['consecutive_wins'].max()
        st.markdown(f"<h4 style='text-align: center;'>Longest Win Streak</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>{longest_win_streak}</p>", unsafe_allow_html=True)
    
    # Avg. Win Margin
    with row5_col1:
        wins = season_data[season_data['win'] == 1].copy()
        wins['win_margin'] = wins['cnu_score'] - wins['opp_score']
        avg_win_margin = '{:.2f}'.format(wins.loc[:, 'win_margin'].mean())
        
        st.markdown(f"<h4 style='text-align: center;'>Average Win Margin</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>{avg_win_margin}</p>", unsafe_allow_html=True)
    # Avg. PPG
    with row5_col2:
        avg_ppg = '{:.2f}'.format(season_data.loc[:, 'cnu_score'].mean())
        
        st.markdown(f"<h4 style='text-align: center;'>Average CNU PPG</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>{avg_ppg}</p>", unsafe_allow_html=True)
    # Avg. Opp PPG
    with row5_col3:
        avg_opp_ppg = '{:.2f}'.format(season_data.loc[:, 'opp_score'].mean())
        
        st.markdown(f"<h4 style='text-align: center;'>Average Opponent PPG</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>{avg_opp_ppg}</p>", unsafe_allow_html=True)
        
    # Home Record
    with row6_col1:
        home = season_data[season_data['home'] == 1].copy()
        home_win, home_loss = home.win.value_counts()

        st.markdown(f"<h4 style='text-align: center;'>Home Record</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>{home_win}-{home_loss}</p>", unsafe_allow_html=True)
    # Away Record
    with row6_col2:
        away = season_data[season_data['home'] == 0].copy()
        away_win, away_loss = away.win.value_counts()
        
        st.markdown(f"<h4 style='text-align: center;'>Away Record</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>{away_win}-{away_loss}</p>", unsafe_allow_html=True)
    
    
    
    # --- GAME DATA ---
    st.subheader(f'Team Stats for {season} Season')

    st.dataframe(data=season_data[table_cols].sort_values('date', ascending=False).set_index('opponent'))