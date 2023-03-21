# Netflix-Recommedations

**What's the idea?**<br>
- Using a dataset of Netflix movies and TV shows (from now on, I will refer to this as "media/medium"), I wanted the user to input the title of a medium (it has to exist in the given dataset), and my program would output a list of the most appropriate/similar media based on description, genre, IMDB rating and MPAA rating.

**What's the data?**<br>
- Netflix dataset is from Kaggle. `https://www.kaggle.com/datasets/shivamb/netflix-shows` The attributes of each medium are a unique id, title, description, director*, list of genres, cast*, production country*, release date*, MPAA rating*, duration*, IMDB score*, content type, and date added*. `*` denotes that there are null values, as a result this project focuses more on title, description, list of genres, MPAA rating, and IMDB score.

**How does it work? (with examples)**<br>
- The overall goal is to quantify how similar medium (A) is to another medium B, essentially turning words (of which the program doesn't know the meaning) into a number [0,1] that represents how similar A and B are. Once we know how to do that, we can repeat the process until we know how similar every medium is every other medium.
- First, I clean the titles, descriptions, and genres by removing punctation and stopwords (which are words that aren't important enough to contribute meaning, such as "the", "and", "was", etc.), changing all the words to use lowercase letters, and reducing all words to their root words (walking and walked would become walk).

>"Annie and Hallie (Lindsay Lohan) are strangers until happenstance unites them. If the scheme works, it might just make the family whole again."

turns into 

>"anni halli lindsay lohan stranger happenst unit scheme work might make famili whole"

- Once the text data is cleaned, we want the frequency of each word. Each medium is a separate entity, and each medium has a title, description, and list of genres.

For the title, description, and genre list of each Netflix medium, we want the frequency of each word, and then make these numbers into vectors. TfidfVectorizer (term frequency-inverse document frequency) does this for us.


## IN PROGRESS
