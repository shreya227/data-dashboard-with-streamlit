import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image

# Original problematic line
if not st.sidebar.checkbox('Close', True, key='1'):
    st.write('Application is open')

# Updated with unique keys
if not st.sidebar.checkbox('Close', True, key='close_checkbox_1'):
    st.write('Application is open')

# Another widget with a unique key
if st.button('Submit', key='submit_button_1'):
    st.write('Button clicked!')


st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('📊 Sentiment Analysis of Tweets about US Airlines')
st.sidebar.title('Sentiment Analysis of Tweets about US Airlines')

st.markdown('This application is a streamlit dashboard to analyze the sentiments of Tweets 🐦')
st.subheader('Dataset')
st.sidebar.markdown('This application is a streamlit dashboard to analyze the sentiments of Tweets 🐦')

DATA_URL = ("Tweets.csv")

@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()  
st.write(data)

st.sidebar.subheader('▪️ Show random tweet')
random_tweet = st.sidebar.radio('Sentiment',('positive','neutral','negative'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[['text']].sample(n=1).iat[0,0])

st.sidebar.markdown("### ▪️ Number of tweets by sentiment")
select = st.sidebar.selectbox('Visualization type:', ['Bar Chart','Pie Chart'], key='1')
sent_count = data['airline_sentiment'].value_counts()
sent_count = pd.DataFrame({'Sentiment':sent_count.index, 'Tweets':sent_count.values})


if not st.sidebar.checkbox('Hide', True):
    st.markdown("### ▪️ Number of tweets by sentiment")
    if select == 'Bar Chart':
        fig = px.bar(sent_count, x='Sentiment',y='Tweets', 
            color='Tweets', height=500)
        st.write(sent_count)
        st.plotly_chart(fig)

    else:
        fig1 = px.pie(sent_count, values='Tweets', names ='Sentiment')
        st.plotly_chart(fig1)
        st.write(sent_count)


st.sidebar.subheader('▪️ When and where are users tweeting from?')
hour = st.sidebar.number_input('Hour of the day',min_value = 1, max_value = 24)
m_d = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox('Close', True, key='1'):
    st.markdown("### ▪️ Tweets locations based on the time of day")
    st.markdown('%i tweets between %i:00 and %i:00' % (len(m_d),hour, (hour+1)%24))
    st.map(m_d)
    if st.sidebar.checkbox('Show raw data', False):
        st.write(m_d)

st.sidebar.subheader('▪️ Breakdown airline tweets by sentiments')
choice = st.sidebar.multiselect('Pick airlines', ('US Airways',
    'United', 'American', 'Southwest','Delta','Virgin America'), key='0')

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment', histfunc='count', color='airline_sentiment'
        , facet_col = 'airline_sentiment', labels={'airline_sentiment':'tweets'}, height=600, width= 800)
    st.plotly_chart(fig_choice)


st.sidebar.header('▪️ Word Cloud')
word_sent = st.sidebar.radio('Display word cloud for what sentiment?', 
    ('positive','neutral','negative'))

if not st.sidebar.checkbox('Close', True, key = '3'):
    st.header('▪️ Word Cloud for %s sentiment' % (word_sent))
    df = data[data['airline_sentiment']== word_sent]
    words = ''.join(df['text'])
    pro_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords= STOPWORDS, background_color='lightblue',height=500, width=800).generate(pro_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()




