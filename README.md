# Netflix-Recommedations

**What's the idea?**<br>
- Using a dataset of Netflix movies and TV shows (from now on, I will refer to this as Netflix media), I wanted the user to input the title of a Netflix medium (it has to exist in the given dataset), and my program would output a list of the most similar Netflix media based on description, genre, IMDB rating and MPAA rating.

**How does it work?**<br>
- The overall goal is to quantify how similar 1 Netflix medium is to another, essentially turning words (of which the program doesn't know the meaning) into a number [0,1] that represents similarity. Once we know how to do that, we can repeat the process until we know how similar every Netflix medium is every other Netflix medium.
- First, I clean the titles, descriptions, and genres by removing punctation and stopwords (which are words that aren't important enough to contribute meaning, such as "the", "and", "was", etc.), changing all the words to use lowercase letters, and reducing all words to their root words (walking and walked would become walk).
- For the title, description, and genre list of each Netflix medium, we want the frequency of each word, and then make these numbers into vectors. TfidfVectorizer (term frequency-inverse document frequency) does this for us.


## IN PROGRESS
