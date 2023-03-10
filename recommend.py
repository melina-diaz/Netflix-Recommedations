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
    
    global data
    data = pd.read_csv("netflixData.csv")
    print("Data loaded")
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
    global titleslist
    titleslist=data["Title"].tolist()
    global titleslower
    titleslower=[x.lower() for x in titleslist]
    print("Data cleaned")

def netflix_recommendation_g(title):
    """genre, then description"""
    similarity1 = similaritygenre
    similarity2=similaritydesc
    index = indices[title]
    similarity_scores = list(enumerate(zip(similarity1[index],similarity2[index])))
    similarity_scores = sorted(similarity_scores, key=lambda x: (x[1][0], x[1][1]), reverse=True)
    test=similarity_scores
    similarity_scores = similarity_scores[1:11]
    movieindices = [i[0] for i in similarity_scores]
    return data[['Title',"Imdb Score", "Rating"]].iloc[movieindices]

def netflix_recommendation_d(title):
    """description, then genre"""
    similarity1 = similaritygenre
    similarity2=similaritydesc
    index = indices[title]
    similarity_scores = list(enumerate(zip(similarity1[index],similarity2[index])))
    similarity_scores = sorted(similarity_scores, key=lambda x: (x[1][1], x[1][0]), reverse=True)
    test=similarity_scores
    similarity_scores = similarity_scores[1:11]
    movieindices = [i[0] for i in similarity_scores]
    return data[['Title',"Imdb Score", "Rating"]].iloc[movieindices]
    
def netflix_recommendation_c(title):
    """linear combo of description and genre"""
    similarity1 = similaritygenre
    similarity2=similaritydesc
    index = indices[title]
    similarity_scores = list(enumerate(zip(similarity1[index],similarity2[index])))
    similarity_scores = sorted(similarity_scores, key=lambda x: (x[1][0]+1.6* x[1][1]), reverse=True)
    test=similarity_scores
    similarity_scores = similarity_scores[1:11]
    movieindices = [i[0] for i in similarity_scores]
    return data[['Title',"Imdb Score", "Rating"]].iloc[movieindices]
  
def netFlix_recommendation(title):
    """only genre, control"""
    similarity = similaritygenre
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
    user=input()
    return

def ask():
    user=input("What is the Netflix movie or TV show?\n")
    while (user.lower() not in titleslower and user.lower()!= "!show" and user.lower()!="!quit"):
        user=input("Your answer was not recognized. Try again. The title has to be included our Netflix database and is case-sensitive. If you want to view our Netflix database, enter '!show'. \n")
    if user == "!show":
        show()
        ask()
    if user == "!quit":
        return #bug
    return user
    
def show():
    user=input("You are viewing our Netflix database. Press any key to continue.\n")
    pd.set_option('display.max_rows', None)
    print(data["Title"])
    pd.reset_option('display.max_columns')
    user=input("")

setup()
user=input("Hi! This is my Netflix recommendation system. If you provide a Netflix TV show or movie, I can give you a list of related Netflix TV shows or movies.\nDo you have a Netflix TV show or movie in mind? (y/n) If not, you can look at the full list of Netflix media that is applicable. \n")
while (user.lower() not in ["yes", "no", "y", "n"]):
    user=input("Your answer was not recognized. Do you have a Netflix TV show or movie that you want to receive recommendations for? (y/n) \n")
if user.lower() in ["no", "n"]:
    show() #yes have a movie or tv show
user=ask()

print("Providing recommendations for", user + ". One moment please." )
compare_fun(user)
ask()

#if there are multiple?
