import numpy as np 
import pandas as pd
import plotly.express as px 
from textblob import TextBlob


df = pd.read_csv('netflix_titles.csv')
df.shape
df.columns
df.head()
x = df.groupby(['rating']).size().reset_index(name='counts')
pieChart = px.pie(x, values='counts', names='rating', title='Distribution of content ratings on Netflix')
pieChart.show()


df['director']=df['director'].fillna('Director not specified')
directors_list=pd.DataFrame()
directors_list = df['director'].str.split(',', expand=True).stack()
directors_list = directors_list.to_frame()
directors_list.columns=['Director']
directors = directors_list.groupby(['Director']).size().reset_index(name='Total Count')
directors = directors[directors.Director != 'Director not specified']
directors = directors.sort_values(by=['Total Count'], ascending=False)
top5Directors = directors.head()
barChart = px.bar(top5Directors, x = 'Total Count', y = 'Director', title = 'top 5 Directors on Netflix')
barChart.show()


df['cast']=df['cast'].fillna('Cast not specified')
casts_list=pd.DataFrame()
casts_list = df['cast'].str.split(',', expand=True).stack()
casts_list = casts_list.to_frame()
casts_list.columns=['Actor']
actors = casts_list.groupby(['Actor']).size().reset_index(name='Total Count')
actors = actors[actors.Actor != 'Cast not specified']
actors = actors.sort_values(by=['Total Count'], ascending=False)
top5Actors = actors.head()
top5Actors = top5Actors.sort_values(by=['Total Count'])
barChart2 = px.bar(top5Actors, x = 'Total Count', y = 'Actor', title = 'top 5 Actors on Netflix')
barChart2.show()


df1 = df[['type', 'release_year']]
df1 = df1.rename(columns = {"release_year":"Relase Year", "type":"Type"})
df2 = df1.groupby(["Relase Year", "Type"]).size().reset_index(name='Total Count')
df2 = df2[df2['Relase Year'] >= 2000]
graph = px.line(df2, x='Relase Year', y='Total Count', color = 'Type', title = "Trend of Content Produced on Netflix Every Year")
graph.show()


df3=df[['release_year', 'description']]
df3=df3.rename(columns = {"release_year":"Relase Year", "description":"Description"})
for index, row in df3.iterrows():
  d=row['Description']
  testimonial = TextBlob(d)
  p = testimonial.sentiment.polarity
  if p ==0:
    sent = 'Neutral'
  elif p>0:
    sent = 'Positive'
  else:
    sent = 'Negative'
  df3.loc[[index, 2], 'Santiment']=sent

df3=df3.groupby(['Relase Year', 'Santiment']).size().reset_index(name="Total Count")

df3=df3[df3['Relase Year']>2005]
barGraph=px.bar(df3, x= "Relase Year", y='Total Count', color = "Santiment", title='Santiment Analysis of Content on Netflix')
barGraph.show()

