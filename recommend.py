import pandas as pd
import numpy as np
from sklearn.feature_extraction import text
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import re
nltk.download('stopwords')
stemmer = nltk.SnowballStemmer("english")
from nltk.corpus import stopwords
import string
stopword=set(stopwords.words('english'))
import itertools

def clean(text):
  text = str(text).lower()
  text = re.sub('\[.*?\]', '', text)
  text = re.sub('https?://\S+|www\.\S+', '', text)
  text = re.sub('<.*?>+', '', text)
  text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
  text = re.sub('\n', '', text)
  text = re.sub('\w*\d\w*', '', text)
  text = [word for word in text.split(' ') if word not in stopword]
  text=" ".join(text)
  text = [stemmer.stem(word) for word in text.split(' ')]
  text=" ".join(text)
  return text

def setup():
  data = pd.read_csv("netflixData.csv")
  print("data loaded")
  data = data[["Title", "Description", "Content Type", "Genres", "Imdb Score", "Rating"]]
  data["Description Clean"]=data["Description"].apply(clean)
  data["Title Clean"] = data["Title"].apply(clean)
  data["Genres"]=data["Genres"].str.replace(' ','_')
  data["Genres"]=data["Genres"].str.replace(',_',', ')
  feature = data["Genres"].tolist()
  tfidf = text.TfidfVectorizer(input=feature, stop_words=None, lowercase=True, token_pattern=r'\w[-\w&\']*\w')
  tfidf_matrix = tfidf.fit_transform(feature)
  global similaritygenre
  similaritygenre= cosine_similarity(tfidf_matrix)
  feature = data["Description Clean"].tolist()
  tfidf = text.TfidfVectorizer(input=feature, stop_words='english')
  tfidf_matrix = tfidf.fit_transform(feature)
  global similaritydesc
  similaritydesc= cosine_similarity(tfidf_matrix)
  global indices
  indices = pd.Series(data.index, index=data['Title']).drop_duplicates()

def netflix_recommendation_g(title, similarity1 = similaritygenre, similarity2=similaritydesc):
  """genre, then description"""
  index = indices[title]
  similarity_scores = list(enumerate(zip(similarity1[index],similarity2[index])))
  similarity_scores = sorted(similarity_scores, key=lambda x: (x[1][0], x[1][1]), reverse=True)
  test=similarity_scores
  similarity_scores = similarity_scores[1:11]
  movieindices = [i[0] for i in similarity_scores]
  return data[['Title',"Imdb Score", "Rating"]].iloc[movieindices]

def netflix_recommendation_d(title, similarity1 = similaritygenre, similarity2=similaritydesc):
  """description, then genre"""
  index = indices[title]
  similarity_scores = list(enumerate(zip(similarity1[index],similarity2[index])))
  similarity_scores = sorted(similarity_scores, key=lambda x: (x[1][1], x[1][0]), reverse=True)
  test=similarity_scores
  similarity_scores = similarity_scores[1:11]
  movieindices = [i[0] for i in similarity_scores]
  return data[['Title',"Imdb Score", "Rating"]].iloc[movieindices]
  
def netflix_recommendation_c(title, similarity1 = similaritygenre, similarity2=similaritydesc):
  """linear combo of description and genre"""
  index = indices[title]
  similarity_scores = list(enumerate(zip(similarity1[index],similarity2[index])))
  similarity_scores = sorted(similarity_scores, key=lambda x: (x[1][0]+1.6* x[1][1]), reverse=True)
  test=similarity_scores
  similarity_scores = similarity_scores[1:11]
  movieindices = [i[0] for i in similarity_scores]
  return data[['Title',"Imdb Score", "Rating"]].iloc[movieindices]
  
def netFlix_recommendation(title, similarity = similaritygenre):
  """only genre, control"""
  index = indices[title]
  similarity_scores = list(enumerate(similarity[index]))
  test=similarity_scores
  similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
  similarity_scores = similarity_scores[0:10]
  movieindices = [i[0] for i in similarity_scores]
  return data['Title'].iloc[movieindices]
  
def compare_fun(title):
  print("genre priority")
  print(netflix_recommendation_g(title))
  print("\ndesc priority")
  print(netflix_recommendation_d(title))
  print("\nlinear combo")
  print(netflix_recommendation_c(title))
  print("\ncontrol")
  print(netFlix_recommendation(title))
  
def show():
  pd.set_option('display.max_rows', None)
  print(data["Title"])
  pd.reset_option('display.max_columns')
