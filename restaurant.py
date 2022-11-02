from unittest import result
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import jieba
from wordcloud import WordCloud 

plt.style.use('seaborn')

df=pd.read_csv('restaurant.csv')
df=df.iloc[:,1:]
df_cities= pd.DataFrame(df.groupby('city').name.count().sort_values(ascending = False))
df_cities.rename(columns={'name':'num'},inplace=True)

st.title('Factors affecting restaurants in Europe')
st.header('Details of Dataset (Take five for example)')
st.write('Have reordered according to the city')
# sample
st.write(df.head())
st.header('Number of Restaurants')

# pie chart
fig0, ax0 = plt.subplots(figsize = (20,20))
ax0.set_title('Pie chart for restaurant numbers')
ax0 = plt.pie(df['city'].value_counts(),labels = df_cities.index,autopct='%3.1f%%')
st.pyplot(fig0)


num_filter = st.slider('Number of Restaurants in each city:',0,17500,2000)  


# filter by num
df_cities = df_cities[df_cities.num >= num_filter]

st.bar_chart(df_cities)


st.header('Q 1: We want to know which cities have many restaurants and the reasons behind this phenomenon.')
st.write('We can see that London and Paris have over 10,000 restaurants. Both of the city are prosperity and energetic. The service sector can develop very well over here. That is the same thing for restaurant business. ')







st.header('Reviews number of Restaurants')
df_reviews = pd.DataFrame(df.groupby('city').reviews_number.sum().sort_values(ascending=False))
reviews_filter = st.slider('Average Reviews number in each city:',10000,2000000,60000) 

df_reviews = df_reviews[df_reviews.reviews_number>= reviews_filter]

st.bar_chart(df_reviews)


st.header('Q 2: We notice that the review number gets a little bit different from restaurant number.')
st.write('We can see that the numbers of review in Rome is higher than Pairs. But Rome\'s restaurant number is much lower than that. It\'s quite interesting. We can guess if the Romans have a more discerning palate. Or French are more unwilling to make comments. But we all konw that French food is a little expensive. Will the cost of cusine be a obstacle for reviews? Taht may be a reason.')



st.header('Price range of Restaurants')
st.write('Use something more intuitive ro replace the notation used in the dataset')

df['price_range'] = df['price_range'].fillna('NA')
price_ranges = {'$': 'Cheaper', '$$ - $$$': 'Medium', '$$$$': 'Higher', 'NA': 'NotAvailable'}
df['price_range'] = df.price_range.map(price_ranges)

st.write(price_ranges)
# st.sidebar.write('setect city you interested ')

st.subheader('Price range of all cities')

fig1, ax1 = plt.subplots(figsize=(8, 6))
df_all=pd.DataFrame(df.groupby(['city', 'price_range']).name.count()).reset_index()

sns.barplot(data=df_all,x='city', y ='name', hue='price_range', hue_order = ['Cheaper', 'Medium', 'Higher'], palette = ['#4ECDC4', '#FFE66D', '#FF6B6B'])
plt.ylabel('Reviews per Price Range')
plt.xticks(rotation=75)
st.pyplot(fig1)

st.subheader('Price range of selected city')

city_filter = st.sidebar.selectbox(
     'City Selector Of Princ_range',
     df.city.unique(),  # options
     1)  # defaults


# filter by capital
df_price = df[df['city']==city_filter]
df_price = pd.DataFrame(df_price.groupby(['city', 'price_range']).name.count()).reset_index()

st.write('Peice range of',city_filter)

fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.barplot(data=df_price,x='city', y ='name', hue='price_range', hue_order = ['Cheaper', 'Medium', 'Higher'], palette = ['#4ECDC4', '#FFE66D', '#FF6B6B'])
plt.ylabel('Reviews per Price Range')
st.pyplot(fig2)

st.header('Cuisine style Analyse')
st.subheader('Cuisine style of Europe')

cuisine=""
for i in df.cuisine_style:
    cuisine+=str(i)
cuisine=cuisine.replace('[','')
cuisine=cuisine.replace(']','')
cuisine=jieba.cut(cuisine)
cuisine=''.join(cuisine)
cuisine=cuisine.replace(',','')

wc=WordCloud(
    background_color="white", 
    width=400, 
    height=300,
    max_words=200, 
    max_font_size=80, 
    contour_width=3, 
    contour_color='steelblue',
    mode='RGBA' 
    
)

fig3=plt.figure(figsize=(8,8))
wc.generate(cuisine)
plt.imshow(wc) 
plt.axis("off")
st.pyplot(fig3)



cuisine_filter = st.sidebar.selectbox(
     'City Selector Of Cuisine',
     df.city.unique(),  # options
     1) 

st.subheader('Cuisine style of Selected City:')
st.write('Cuisine style of',cuisine_filter)
df_cuisine = df[df['city']==cuisine_filter]

cuisine_=""
for i in df_cuisine.cuisine_style:
    cuisine_+=str(i)
cuisine_=cuisine_.replace('[','')
cuisine_=cuisine_.replace(']','')
cuisine_=jieba.cut(cuisine_)
cuisine_=''.join(cuisine)
cuisine_=cuisine_.replace(',','')

wc=WordCloud(
    background_color="white", 
    width=400, 
    height=300,
    max_words=200, 
    max_font_size=80, 
    contour_width=3, 
    contour_color='steelblue',
     mode='RGBA' 
    
)

fig4=plt.figure(figsize=(8,8))
wc.generate(cuisine_)
plt.imshow(wc) 
plt.axis("off")
st.pyplot(fig4)
