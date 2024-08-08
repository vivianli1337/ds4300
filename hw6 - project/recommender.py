from pymongo import MongoClient

class Recommender:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['movies_db']
        self.movies_collection = self.db['movies_cl']

    def get_movie_recommendations(self, movie_title):
        # Fetch the movie data from MongoDB
        movie = self.movies_collection.find_one({'title': movie_title})
        if movie:
            # Retrieve the pre-calculated recommended movie IDs
            recommended_movie_ids = movie.get('recommendations', [])
            # Fetch the recommended movie data from MongoDB
            recommended_movies = self.movies_collection.find({'_id': {'$in': recommended_movie_ids}}).sort('popularity', -1)
            return list(recommended_movies)
        else:
            return []

    def get_keyword_recommendations(self, keywords):
        # Perform a text search on the 'keywords' field
        query = {'keywords': {'$in': keywords.split()}}
        recommended_movies = self.movies_collection.find(query).sort('popularity', -1)
        return list(recommended_movies)

    def get_genre_recommendations(self, genres):
        # Find movies that match the specified genres
        query = {'genres': {'$in': genres}}
        recommended_movies = self.movies_collection.find(query).sort('popularity', -1)
        return list(recommended_movies)

    def get_year_recommendations(self, year):
        # Find movies released in the specified year
        query = {'release_date': {'$regex': f'^{year}'}}
        recommended_movies = self.movies_collection.find(query).sort('popularity', -1)
        return list(recommended_movies)

    def get_actor_recommendations(self, actor):
        # Find movies featuring the specified actor
        query = {'credits': actor}
        recommended_movies = self.movies_collection.find(query).sort('popularity', -1)
        return list(recommended_movies)

    def get_language_recommendations(self, language):
        # Find movies in the specified language
        query = {'original_language': language}
        recommended_movies = self.movies_collection.find(query).sort('popularity', -1)
        return list(recommended_movies)

    def get_all_movies(self):
        # Fetch all movies from MongoDB
        all_movies = self.movies_collection.find({}).sort('popularity', -1)
        return list(all_movies)

    def get_all_genres(self):
        # Fetch all distinct genres from MongoDB
        all_genres = self.movies_collection.distinct('genres')
        return list(all_genres)

    def get_all_languages(self):
        # Fetch all distinct original languages from MongoDB
        all_languages = self.movies_collection.distinct('original_language')
        return list(all_languages)
    
    def filter_movies(self, movie_title, keywords, genres, year, actor, language):
        # Apply filters to fetch filtered movies
        query = {}
        if movie_title:
            query['title'] = {'$regex': movie_title}
        if keywords:
            query['keywords'] = {'$in': keywords.split()}
        if genres:
            query['genres'] = {'$in': genres}
        if year:
            query['release_date'] = {'$regex': f'^{year}'}
        if actor:
            query['credits'] = actor
        if language:
            query['original_language'] = language

        filtered_movies = self.movies_collection.find(query)
        return list(filtered_movies)