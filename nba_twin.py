# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 10:35:39 2023

@author: David
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
st.set_page_config(page_title='BBL Twin Player',initial_sidebar_state="expanded",page_icon='basketball.jpg')


def nba_twin(bbl_player,bbl_team='None'):
    if bbl_team == 'None':
        scaled_lat_features['tmp']=np.linalg.norm((scaled_lat_features_bbl.loc[bbl_player].values-scaled_lat_features.values[:,:-1]),axis=1)
        result= scaled_lat_features['tmp'].idxmin()
        scaled_lat_features.drop(columns='tmp',axis=1,inplace=True)
    else:
        scaled_lat_features['tmp']=np.linalg.norm((scaled_lat_features_bbl.loc[(bbl_player, bbl_team)].values-scaled_lat_features.values[:,:-1]),axis=1)
        result= scaled_lat_features['tmp'].idxmin()
        scaled_lat_features.drop(columns='tmp',axis=1,inplace=True)
    return result


def load_teams():
    with open('nba_teams.json','r') as f:
        teams_nba=json.load(f)
        return teams_nba

#@st.cache    
def load_data1():
    df=pd.read_csv('.scaled_lat_features.csv',index_col=['Player','Team'])
    return df
#@st.cache
def load_data2():
    df=pd.read_csv('.scaled_lat_features_bbl.csv',index_col=['Player','Team'])
    return df


scaled_lat_features = load_data1()
scaled_lat_features_bbl=load_data2()
nba_teams=load_teams()

#scaled_lat_features_bbl.xs('Würzburg Baskets', level=1, drop_level=False).index.get_level_values(0)
options=list(scaled_lat_features_bbl.index.get_level_values(1).unique())
options.insert(0,'League')
len(options)
side_bar=st.sidebar
side_bar.subheader('Select first a Team or the whole League, then some Players!')
team=side_bar.selectbox('Choose the Team:',options)

if team == 'League':
    team='None'
    players=list(scaled_lat_features_bbl.index.get_level_values(0))
    player=side_bar.multiselect(f'Now Choose one or more Players from the BBL',players)
else:
    players=list(scaled_lat_features_bbl.xs(team, level=1, drop_level=False).index.get_level_values(0))
    player=side_bar.multiselect(f'Now Choose one or more Players from {team}',players)
#players=list(scaled_lat_features_bbl.xs(team, level=1, drop_level=False).index.get_level_values(0))
#p=st.container()
st.header ("BBL Player's NBA Twin")
#st.markdown('''<style>.div-1{background-color: DarkBlue;color:white} </style> <div class="div-1"> <b>The App finds the most similar NBA Player from Season 2021/2022 to recent BBL Players. </b> </div>''', unsafe_allow_html=True)
st.markdown("<b>This App finds the most similar playstyle NBA Player from Season 2021/2022 to recent BBL Players*. </b>" , unsafe_allow_html=True)
st.write(''' <small>*BBL Players with > 9 Games played at February 23 are available. </small>''',unsafe_allow_html=True)
 

st.write('''Turn any [BBL-Player](https://www.easycredit-bbl.de/statistiken/spieler) \
         into his *Playstyle Twin* [NBA-Player](https://www.nba.com/players). <br> \
         Navigate the <b> Playstyle-Matching </b> over the sidebar menu.''',unsafe_allow_html=True)
with st.expander('Description'):
    st.write('''<p>The underlying algorithm maps NBA players based on their stats and advanced metrics into latent styles of play. \
            Then BBL players are projected in this latent space and the similarity is calculated to each NBA player. <br> \
             </p>''', unsafe_allow_html=True )

#st.markdown('''<p style = "background-color: DarkBlue;color:white;">The underlying algorithm maps NBA players based on their Stats and advanced metrics into latent styles of play. Then BBL players are projected in this latent space and the similarity is calculated to each NBA player.</p>''', unsafe_allow_html=True )
submit=side_bar.button('Show results')
if submit:
    res={}
    for pl in player:
        res[pl]=nba_twin(pl,team)
        st.success(f'The most similar NBA Player of {pl} is {res[pl][0]} from {nba_teams[res[pl][1]]}.')
    side_bar.warning('If you are on a mobile device close the Sidebar to see the results')
side_bar.info(':information_source: For more Infos contact me: dgfin@gmx.de ')


mp=st.empty()
mp.success("If you run the NBA_Twin algorithm for TJ Shorts II, it suggests Trae Young as his NBA-Twin  \
        (Test this by yourself :male-teacher: )")
mp2=st.empty()
with mp2.expander('See  TJ Shorts II and Trae Young in action '):
    colA,colB =st.columns(2)
    with colA:
        #videoA=open('https://www.youtube.com/watch?v=LDJWGvX7-eE','rb')
        #videoA_bytes=videoA.read()
        st.video('https://www.youtube.com/watch?v=LDJWGvX7-eE')
        
    with colB:
        st.video('https://www.youtube.com/watch?v=8P9ZYfQSVMY')

if submit:
    mp.empty()
    mp2.empty()


st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")
col1, col2=st.columns(2)  

with col1:
    st.markdown(''' <h3 id="Metrics"> Stats </h3>''',unsafe_allow_html=True)
    st.markdown('Several available stats of the BBL-Players were collected. Based on those stats \
                advanced metrics including True Shooting, Usage Rate, Offensive and Defensive Win Shares, \
                Points per Possession were computed. More information on those metrics and their computation \
                can be found on  [this nice page](https://www.basketball-reference.com/about/). \
                The corresponding stats were collected for NBA-Players from Season 2021/2022.\
                Based on those stats the same computations were made. Altogether the dataset contained more than 40 features.')
    
with col2:
    st.markdown(''' <h3 id="Algorithm"> Algorithm </h3>''',unsafe_allow_html=True)
    st.markdown("Each NBA Player is represented by his stats and advanced metrics. \
                For his playstyle the algorithm determines a  number of latent features and maps the original \
                features in the latent feature space.\
                  The BBL-Players are \
                projected in this new space of latent features. For \
                 instance those might stand for\
                short-distance shooting, long-distance shooting, passing, defending,\
                physical ability, speed, role in the team ... . More details \
                 on the underlying technique  \
            can be found   \
            [in this book](https://link.springer.com/book/10.1007/978-3-662-62521-7).")
    
    
