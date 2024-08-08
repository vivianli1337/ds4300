from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
import numpy as np

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['movies_db']
collection = db['movies_cl']

# Function to calculate total number of movies
def get_total_movies():
    return collection.count_documents({})

# Distribution of movie genres
def analyze_genre_distribution():
    # Fetch genre data from MongoDB
    genres = collection.distinct('genres')

    # Count occurrences of each genre
    genre_counts = {}
    for genre in genres:
        count = collection.count_documents({'genres': genre})
        genre_counts[genre] = count

    # Check for missing genre label and replace with "Unknown"
    if '' in genre_counts:
        unknown_count = genre_counts.pop('')
        genre_counts['Unknown'] = unknown_count

    # Sort genre counts by values
    sorted_genre_counts = dict(sorted(genre_counts.items(), key=lambda item: item[1], reverse=True))

    # Plot genre distribution
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x=list(sorted_genre_counts.values()), y=list(sorted_genre_counts.keys()), color='cadetblue')

    for i, count in enumerate(sorted_genre_counts.values()):
        ax.text(count + 3, i, str(count), va='center')

    plt.xlabel('Number of Movies')
    plt.ylabel('Genre')
    plt.title(f'Distribution of Movie Genres (Total Movies: {get_total_movies()})')
    plt.show()

# Average movie rating by year
def analyze_average_rating_by_year():
    # Fetch release years and corresponding average ratings
    pipeline = [
        {"$group": {"_id": "$release_date", "avg_rating": {"$avg": "$vote_average"}}},
        {"$sort": {"_id": 1}}
    ]
    results = list(collection.aggregate(pipeline))
    years = [result['_id'][:4] for result in results]
    avg_ratings = [result['avg_rating'] for result in results]

    # Plot average rating by year
    plt.figure(figsize=(10, 6))
    plt.plot(years, avg_ratings, marker='o', markersize=4)
    plt.xlabel('Year')
    plt.ylabel('Average Rating')
    plt.title(f'Average Movie Rating by Year (Total Movies: {get_total_movies()})')
    plt.xticks(rotation=90, size=10)
    plt.grid(True)
    plt.show()

# Function to analyze language distribution
def analyze_language_distribution():
    # Fetch language data from MongoDB
    languages = collection.distinct('original_language')

    # Count occurrences of each language
    language_counts = {}
    for language in languages:
        count = collection.count_documents({'original_language': language})
        language_counts[language] = count

    # Create a DataFrame for Plotly
    data = {'Language': list(language_counts.keys()), 'Count': list(language_counts.values())}
    df = pd.DataFrame(data)

    # Calculate percentages
    df['Percentage'] = df['Count'] / df['Count'].sum() * 100

    # Create an interactive pie chart using Plotly
    fig = px.pie(df, values='Count', names='Language', hover_data=['Percentage'],
                 title=f'Language Distribution of Movies (Total Movies: {get_total_movies()})',
                 labels={'Language': 'Language'})  
    
    # Move legend outside of the pie chart
    fig.update_layout(legend=dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="right",
        x=1.2
    ))

    # Show the plot
    fig.show()

# Function to retrieve budget, revenue, and average rating data
def get_budget_revenue_rating_data():
    cursor = collection.find({}, {'_id': 0, 'budget': 1, 'revenue': 1, 'vote_average': 1})
    budget_revenue_rating_data = [(record['budget'], record['revenue'], record['vote_average']) for record in cursor]
    return budget_revenue_rating_data

# Function to create scatter plot
def analyze_budget_revenue():
    budget_revenue_rating_data = get_budget_revenue_rating_data()
    budgets, revenues, ratings = zip(*budget_revenue_rating_data)

    # Define colors based on the average rating
    colors = np.array(ratings)

    plt.figure(figsize=(10, 6))
    plt.scatter(budgets, revenues, c=colors, cmap='inferno', alpha=0.5)
    plt.colorbar(label='Average Rating')
    plt.title('Relationship between Movie Budgets and Revenues')
    plt.xlabel('Budget ($ in 100 million)')
    plt.ylabel('Revenue ($ in billion)')
    plt.grid(True)


    plt.show()

# Function to retrieve data on actors and their appearances
def get_actor_popularity_data():
    cursor = collection.find({}, {'_id': 0, 'credits': 1})
    actor_list = [record['credits'] for record in cursor if 'credits' in record]
    return actor_list

# Function to calculate frequency of actor appearances
def calculate_actor_frequency(actor_list):
    actor_frequency = {}
    for actors in actor_list:
        for actor in actors:
            if actor in actor_frequency:
                actor_frequency[actor] += 1
            else:
                actor_frequency[actor] = 1
    return actor_frequency

# Function to generate word cloud
def generate_word_cloud(actor_frequency):
    wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='Pastel1').generate_from_frequencies(actor_frequency)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title('Actor Popularity Based on Movie Appearances')
    plt.axis('off')
    plt.show()


# Perform analysis
def main():
    actor_list = get_actor_popularity_data()
    actor_frequency = calculate_actor_frequency(actor_list)
    generate_word_cloud(actor_frequency)

    analyze_genre_distribution()
    analyze_average_rating_by_year()
    analyze_language_distribution()
    analyze_budget_revenue()

main()