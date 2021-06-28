import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px
from add_data import db_execute_fetch

st.set_page_config('Twitter Data Analysis', layout="wide")
st.title('Twitter Data Analysis')

def loadData():
    query = "select * from Tweetsinfo"
    df = db_execute_fetch(query, dbName="Twitter", rdf=True)
    return df 

def text_category(p):
    if p > 0 : return 'positive'
    elif p == 0: return 'neutral'
    return 'negative'


def display_df_polarity(p):
    df = loadData()
    df['score'] = df['polarity'].apply(text_category)
    if p == 'positive':
        st.write(df[df['score'] == 'positive'])
    elif p == 'negative':
        st.write(df[df['score'] == 'negative'])
    elif p == 'neutral':
        st.write(df[df['score'] == 'neutral'])
    else:
        st.write(df)
   
def polarity_count():
    df = loadData()
    df['score'] = df['polarity'].apply(text_category) 
    score = list(df['score'])
    return { 'positive': score.count('positive'), 'neutral': score.count('neutral'),
                            'negative': score.count('negative')  } 


def barChart():
    st.title('Bar Chart visualization')
    count = polarity_count()
    data = pd.DataFrame({
    'Sentiment': list(count.keys()),
    'Tweets': [count[key] for key in count.keys()],
                })
    bar_fig = px.bar(data, x='Sentiment', y='Tweets')
    st.plotly_chart(bar_fig)


def pieChart():
    st.title('Pie Chart visualization')
    count = polarity_count()
    pie_fig = px.pie(values=[count[key] for key in count.keys()], names=list(count.keys()))
    st.plotly_chart(pie_fig)


def wordCloud():
    df = loadData()
    df['original_text'] = df['original_text'].map(lambda x: x.lower())
    long_string = ','.join(list(df['original_text'].values))

    wordcloud = WordCloud(background_color="yellow", width=650, height=450, \
                             min_font_size=5, contour_color='steelblue')
    
    wordcloud.generate(long_string)
    st.title("Word cloud visualization")
    st.image(wordcloud.to_array())

polarity = st.sidebar.selectbox('choose polarity of tweets', ('All', 'positive', 'negative', 'neutral'))
display_df_polarity(polarity)


st.title("Data Visualizations")
visualization = st.sidebar.selectbox('Choose visualization type', 
                ('Word cloud','Bar Chart','Pie Chart'))
if visualization == 'Word cloud':
    wordCloud()
elif visualization == 'Bar Chart':
    barChart()
elif visualization == 'Pie Chart':
    pieChart()