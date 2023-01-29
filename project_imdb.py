import streamlit as st
import pandas as pd

st.title('what to watch?!')
st.subheader('Find your desired movie among 1000 titles:')
'--------'

movies = pd.read_csv('IMDB-Movie-Data.csv')

# create UI
search_type = st.radio('how to search movie?',
                       ['title','other filters'])

if search_type == 'title':
    user_title = st.text_input('movie name')
    conditions = movies['Title'].str.lower().str.contains(user_title)
else:
    [user_year_1, user_year_2] = st.slider('year',
                                           min_value=2005,
                                           max_value=2016,
                                           value=(2007, 2014))
    year_condition = (movies['Year'] >= user_year_1) & (movies['Year'] <= user_year_2)

    user_rating = st.number_input('rate',
                                  min_value=2.0,
                                  max_value=10.0,
                                  step=0.5)
    rate_condition = movies['Rating'] >= user_rating

    conditions = year_condition & rate_condition

    def repp(string):
        return string.split(',')
    genre_series = movies['Genre'].apply(repp)
    set_genres = set()
    for genre_list in genre_series:
        for g in genre_list:
            set_genres.add(g.strip())

    user_genre = st.selectbox('select genre', set_genres)
    if user_genre:
        genre_condition = movies['Genre'].str.contains(user_genre)
        conditions = conditions & genre_condition

    def repp(string):
        return string.split(',')
    actor_series = movies['Actors'].apply(repp)
    set_actors = set()
    for actor_list in actor_series:
        for act in actor_list:
            set_actors.add(act.strip())

    user_actors = st.multiselect('select actors', set_actors)
    if len(user_actors) >0:
        act_condition = movies['Actors'].str.contains(user_actors[0])
        for user_act in user_actors:
            act_condition = act_condition & movies['Actors'].str.contains(user_act)

        conditions = conditions & act_condition

df = movies[conditions]
st.write('number of movies found:',len(df))
df
