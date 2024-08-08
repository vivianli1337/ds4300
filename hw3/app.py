from pymongo import MongoClient
from queries_api import *
import matplotlib.pyplot as plt

client = MongoClient('localhost', 27017)
db = client['RestaurantsDB']
collection = db['restaurants']

# Question 1
print('Question 1 - Find the number of restaurants in each borough that have a grade input by the user')
grades = ['A', 'B', 'C']
get_borough_counts_above_grade(collection, grades)

# Question 2
print('Question 2 - Print the location of the top ___ restaurants in the database')
n=10
find_top_restaurants_and_plot_locations(collection, n)

# Question 3
print("Question 3: Count restaurants that have received at least one 'A' grade and at least one 'B' grade")
count_restaurants_with_grades_and_plot(collection, ['A', 'B'])

# Question 4
print('Question 4 - Find all the [cuisine] restaurants in [borough name] that have a grade input by the user')
find_cuisine(collection, 'Japanese', 'Queens', 'B')

# Question 5
print('Question 5: Count the number of restaurants in each cuisine category in [specific borough] with an average grade []')
count_restaurants(collection, 'B', ['American', 'Mexican', 'Russian', 'Korean', 'Indian'], 'Brooklyn')

# Question 6
print('Question 6: Find restaurants that have improved their score by at least 10 points')
for restaurant in find_improved_restaurants(collection):
    print(restaurant)

# Question 7
print('Question 7: Count the number of restaurants in each cuisine category')
for count in count_cuisines(collection):
    print(count)

# Question 8
print("Question 8: Find restaurants that have never received a grade below 'B'")
for restaurant in find_high_grade_restaurants(collection):
    print(restaurant["name"])

# Question 9
print('Question 9: Find the restaurant with the most number of grades')
for restaurant in find_most_grades_restaurant(collection):
    print(restaurant)

# Question 10
print("Question 10: Calculate the average grade score for Brooklyn and Queens")
for score in calculate_average_score_by_borough(collection):
    print(score)