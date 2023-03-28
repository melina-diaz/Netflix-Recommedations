# Netflix-Recommedations

### **What's the idea?**<br>
Using a dataset of Netflix movies and TV shows (from now on, I will refer to this as "media/medium"), I wanted the user to input the title of a medium (it has to exist in the given dataset), and my program would output a list of the most appropriate/similar media based on description, genre, IMDB rating and MPAA rating.

### **What's the data?**<br>
Netflix dataset is from Kaggle. `https://www.kaggle.com/datasets/shivamb/netflix-shows` The attributes of each medium are a unique id, title, description, director*, list of genres, cast*, production country*, release date*, MPAA rating*, duration*, IMDB score*, content type, and date added*. `*` denotes that there are null values, as a result this project focuses more on title, description, list of genres, MPAA rating, and IMDB score.

### **How does it work? (with examples)**<br>
#### The Short Version
The overall goal is to quantify how similar medium (A) is to another medium (B) with a number [0,1] (meaning between 0 and 1, inclusive). This number or similarity score is calculated using a linear combination of a similarity score between A's description and B's description and a similarity score between A's genre list and B's genre list. The main bulk of this program is quantifying similarity between text, essentially turning text into numbers. Once we know how to do that, we can repeat that process not just between medium A and medium B, but until we know how similar every medium is every other medium. Below is an more in-depth explanation.

#### The Long, More Technical Version
- First, I clean the titles, descriptions, and genres by removing punctation and stopwords (which are words that aren't important enough to contribute meaning, such as "the", "and", "was", etc.), changing all the words to use lowercase letters, and reducing all words to their root words (walking and walked would become walk).

>"Annie and Hallie (Lindsay Lohan) are strangers until happenstance unites them. If the scheme works, it might just make the family whole again."

turns into 

>"anni halli lindsay lohan stranger happenst unit scheme work might make famili whole"

- Once the text data is cleaned, we want the frequencies of each word in each medium's description and genre list. We will store all these frequencies in a term frequency-inverse document frequency (TF-IDF) matrix. A term meaning a word, and a document meaning a medium. An alphabetical list of words that show up in all the mediums' descriptions makes up a master list. For each word in the master list, there will be a number for how many times that word comes up in that medium. We do this for every medium. Then repeat the process with the genres, which will have their own master list, which is much shorter. At the end we will have 2 TF-IDF matrices. The description TF-IDF matrix will have the master list from left to right, and the mediums from top to bottom. So if there M mediums and W words, the matrix will be MxW. Technically, we will have M W-length lists (also called vectors). So these vectors exist in W-dimensions. It might help to visualize these vectors 

- We would then use a cosine similarity function (which is very similar to a dot product) to find the angle and therefore description similarity score for every pair of mediums. This would be 1 number for every 

For the title, description, and genre list of each Netflix medium, we want the frequency of each word, and then make these numbers into vectors. TfidfVectorizer (term frequency-inverse document frequency) does this for us.

**Room for Improvement**
- Fix recommendation algorithm to know what to do when user inputs a medium in which there exists multiple with the same title.
- Use Netflix API to call real-time Netflix media catalog instead of relying on outdated catalog.
- Allow users to input a medium, and it gives attributes and recommendations, therefore user can traverse program like a web.
- Allow a way for user to input a list of media as input.
- Perform network analysis in terms of (basic) count by genre, average IMDB, count cast and director, (advanced) centrality scores by recommendations, clusters.

**How to use**
-

### Credits
Code and ReadMe written by Melina Diaz
