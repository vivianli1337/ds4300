import csv
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['movies_db']
collection = db['movies_cl']

# Clear the existing data in the collection
collection.delete_many({})

# Read the CSV file and insert the data into MongoDB
with open('/Users/vivianli/Downloads/mov/movies.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    movies = []
    limit = 1000  # Limit the number of movies to 10,000
    for row in csv_reader:
        if len(movies) >= limit:
            break
        try:
            movie = {
                'id': row['id'],
                'title': row['title'],
                'genres': row['genres'].split('-'),
                'original_language': row['original_language'],
                'overview': row['overview'],
                'popularity': float(row['popularity']),
                'production_companies': row['production_companies'].split('-'),
                'release_date': row['release_date'],
                'budget': float(row['budget']),
                'revenue': float(row['revenue']),
                'runtime': float(row['runtime']),
                'status': row['status'],
                'tagline': row['tagline'],
                'vote_average': float(row['vote_average']),
                'vote_count': round(float(row['vote_count'])),
                'credits': row['credits'].split('-'),
                'keywords': row['keywords'].split('-'),
                'poster_path': row['poster_path'],
                'backdrop_path': row['backdrop_path'],
            }
            movies.append(movie)
        except (ValueError, KeyError):
            # Skip rows with missing or improper data
            continue

# Insert the movies into the collection
print(len(movies))
collection.insert_many(movies)
print("Data uploaded successfully.")

def process_data(all_movies, similarity_scores, num_movies):
    for i in range(num_movies):
        print(f"Calculating similarity scores for movie {i+1}/{num_movies}")
        movie_id = all_movies[i]['_id']
        similar_indices = similarity_scores[i].argsort()[::-1][1:21]
        recommended_movies = [all_movies[j]['_id'] for j in similar_indices]
        collection.update_one(
            {'_id': movie_id},
            {'$set': {'recommendations': recommended_movies}}
        )

# Calculate similarity scores and store recommendations
def calculate_similarity_scores():
    # Fetch all movies from MongoDB
    all_movies = list(collection.find({}))
    
    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    
    # Prepare the text data for vectorization
    text_data = []
    for movie in all_movies:
        genres = ' '.join(movie['genres'])
        overview = movie['overview']
        keywords = ' '.join(movie['keywords'])
        text = genres + ' ' + overview + ' ' + keywords
        text_data.append(text)
    
    # Fit and transform the text data
    tfidf_matrix = vectorizer.fit_transform(text_data)
    
    # Calculate cosine similarity
    similarity_scores = cosine_similarity(tfidf_matrix)
    
    # Process the entire dataset without batching
    num_movies = len(all_movies)
    process_data(all_movies, similarity_scores, num_movies)
    
    print("Similarity scores calculated and recommendations stored successfully.")

# Calculate similarity scores and store recommendations
calculate_similarity_scores()

