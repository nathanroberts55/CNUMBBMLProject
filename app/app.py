import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="CNU Basketball Data Dashboard",
    page_icon=":basketball:",
    layout='wide',
    initial_sidebar_state='collapsed'
)

# ---- DATA IMPORT ----
@st.cache
def get_data():
    df = pd.read_csv('output/csv/cleaned_data.csv')
    return df

data = get_data()

# ---- DATA HEADER ----
st.sidebar.header('CNU Data Data Dashboard')

st.title('CNUMBB Data Dashboard')
st.markdown(" --- ")

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


with row1_col1:
    total_rebs_chart = px.bar(prev_games, 
                          y=['tot', 'opp_tot'], 
                          x='opponent',
                          barmode='group', 
                          labels={"variable": "Team"}, 
                          hover_data=['off', 'def','opp_off', 'opp_def'],
                          title='Total Rebounds Per Last 5 Games')
    total_rebs_chart.update_layout(xaxis_title='Game', 
                               yaxis_title='Total Rebounds')
    
    st.plotly_chart(total_rebs_chart)
    
with row1_col2:
    total_turnover_chart = px.bar(prev_games, y=['t/o', 'opp_t/o'], 
       x='opponent', 
       barmode='group', 
       labels={"variable": "Team"}, 
       title='Total Turnovers Per Last 5 Games')
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
                         title='Shot Makeup Over Last 5 Games')
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

table_cols = [
 'opponent','date','cnu_score','opp_score','ast','fg%','fga','fgm','3fgm','3fga','3pt%','ft%','fta','ftm','def','off','tot','pf','stl','t/o','blk','opp_ast','opp_fg%','opp_fga','opp_fgm','opp_3fgm','opp_3fga','opp_3pt%','opp_ft%','opp_fta','opp_ftm','opp_def','opp_off','opp_tot','opp_pf','opp_stl','opp_t/o','opp_blk','ast_diff','fg%_diff','fga_diff','fgm_diff','3fga_diff','3fgm_diff','3pt%_diff','ft%_diff','fta_diff','ftm_diff','def_diff','off_diff','tot_diff', 'pf_diff','stl_diff','t/o_diff','blk_diff'
]
st.dataframe(data=data[table_cols].sort_values('date', ascending=False).set_index('opponent'))