import altair as alt
from altair import datum
import pandas as pd
import requests
import io
import streamlit as st
import seaborn as sns

animes = pd.read_csv('anime.csv')
source = pd.read_csv('source.csv')
genre = pd.read_csv('genre.csv')

# Title
st.title('SI 507 presentation')

# Visualization 1: anime genre change over time

# preprocess
animes['category'] = animes.genres.str.split('+')
animes_category_year = animes.loc[:, ['id','year', 'category']].explode('category')
animes_total_year = animes_category_year.groupby('year').agg(['count'])
animes_total_year_category = animes_category_year.groupby(['year', 'category']).agg(['count'])
animes_total_year = animes_total_year.drop(('id', 'count'), axis=1)
animes_percentage_year_category = animes_total_year_category.join(animes_total_year, on='year')
animes_percentage_year_category['percent'] = animes_percentage_year_category[("id", "count")] / animes_percentage_year_category[("category", "count")]
animes_percentage_year_category = animes_percentage_year_category.loc[:,['percent']].reset_index()
animes_percentage_year_category.columns = animes_percentage_year_category.columns.get_level_values(0)

# make visualization
vis_genre_change = alt.Chart(animes_percentage_year_category).mark_bar().encode(
    x = 'year:T',
    y = 'percent:Q',
    color= 'category:N',
    tooltip=['category', 'percent']
).interactive()

# Visualization 2: anime source change over time

# preprocess
animes_source_year = animes.loc[:, ['id','year', 'source']]
animes_total_year = animes_source_year.groupby('year').agg(['count'])
animes_total_year_source = animes_source_year.groupby(['year', 'source']).agg(['count'])
animes_total_year = animes_total_year.drop(('id', 'count'), axis=1)
animes_percentage_year_source = animes_total_year_source.join(animes_total_year, on='year')
animes_percentage_year_source['percent'] = animes_percentage_year_source[("id", "count")] / animes_percentage_year_source[("source", "count")]
animes_percentage_year_source = animes_percentage_year_source.loc[:,['percent']].reset_index()
animes_percentage_year_source.columns = animes_percentage_year_source.columns.get_level_values(0)

# make visualization
vis_source_change = alt.Chart(animes_percentage_year_source).mark_bar().encode(
    x = 'year:T',
    y = 'percent:Q',
    color= 'source:N',
    tooltip = ['source', 'percent']
).interactive()

# Visualization 3: anime broadcast time change over time

# preprocess
animes['hour'] = animes['start_time'].str.split(":").str.get(0)
animes_hour_year = animes.loc[:, ['id','year', 'hour']]
animes_total_year = animes_hour_year.groupby('year').agg(['count'])
animes_total_year_hour = animes_hour_year.groupby(['year', 'hour']).agg(['count'])
animes_total_year = animes_total_year.drop(('id', 'count'), axis=1)
animes_percentage_year_hour = animes_total_year_hour.join(animes_total_year, on='year')
animes_percentage_year_hour['percent'] = animes_percentage_year_hour[("id", "count")] / animes_percentage_year_hour[("hour", "count")]
animes_percentage_year_hour = animes_percentage_year_hour.loc[:,['percent']].reset_index()
animes_percentage_year_hour.columns = animes_percentage_year_hour.columns.get_level_values(0)

# make visualization
vis_broadcast_time_change = alt.Chart(animes_percentage_year_hour).mark_bar().encode(
    x = 'year:T',
    y = 'percent:Q',
    color= 'hour:N',
    tooltip = ['hour', 'percent']
).interactive()

# Visualization 4: bilibili user preference
vis_bilibili_source = alt.Chart(source).mark_bar().transform_aggregate(
    mean_popularity = 'mean(popularity)',
    groupby = ['source']
).encode(
    x = 'source:N',
    y = 'mean_popularity:Q'
).interactive()

vis_bilibili_genre = alt.Chart(genre).mark_bar().encode(
    x = alt.X('popularity', bin=True),
    y = 'count(*):Q',
    color = 'genre:N',
    tooltip=['genre', 'count(*):Q']
).interactive()

vis_bilibili = vis_bilibili_source & vis_bilibili_genre

# make choices
choice = st.sidebar.selectbox(label="Select a visualization to display",options=[
    'anime produced every year',
    'anime genre percentage change over time',
    'anime source percentage change over time',
    'anime broadcast time percentage change over time',
    'bilibili user preference'
])

if choice == 'anime produced every year':

    sns.distplot(animes.loc[:, "year"])
    st.pyplot()
    st.write('''Overall, we see an exponential increase in anime number over time.
    One interesting finding here: there'are several outstanding peaks which are remarkably higher than their neighbors.
    Between peaks, anime number changes slowly; however, after peaks anime number would see an obvious leap.
    ''')
elif choice == 'anime genre percentage change over time':
    vis_genre_change
    st.write('''From the above visualization, we can see clearly the evolvement of anime categories. More categories appeared over the time, and some categories to be the mainstream nowadays.
        Usually an anime has one or two main categories and several other sub-categories. Some categories appear to be mainstream, while others occupy very little percentage. 
        By my observation, mainstream categories include: action, adventure, comedy, slice of life, fantasy, kids.
        Sub-categories are more detailed, and relate to the plot of an anime. Important sub-categories include music, mecha, sci-fi, school, romance, shounen, super-power, etc.
        An interesting observation: comeday is becoming more popular over the years, while adventure is becoming less. Percentage of animes made particularly for kids is shrinking. I would rather say this is because of the rapid growth of adult-level animes. More animes target at teenagers and adults.
    ''')
elif choice == 'anime source percentage change over time':
    vis_source_change
    st.write('''Animes sourced from manga are decreasing, while more original animes are created. Game, light_novel also become important sources nowadays.
    ''')
elif choice == 'anime broadcast time percentage change over time':
    vis_broadcast_time_change
    st.write('''Wow! So there's really a huge change. In the early days of animes, broadcast time is usually around 17:00 - 19:00. However, starting from around 2000, most of animes only broadcast around 22:00-2:00, that's midnight! Though I've heard of this, it's astonishing to see the real data.
    This phenomenan reveal the fact that social impact of anime is decreasing.
    ''')
else:
    vis_bilibili
    st.write('''From the visualization, we can see bilibili users show obvious preference over manga and novel sourced anime.
    They also prefer to watch action / adventure / fantasy anime, while don't prefer kids / shounen ai / club / cars.
    Another takeaway: most anime have low popularity. Only a small portion are extremely popular.
    ''')