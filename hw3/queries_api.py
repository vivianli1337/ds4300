"""
queries_api.py
descriptions: API methods (functions) that allow a scientist to “query” the data
"""
import visualizations

def get_borough_counts_above_grade(collection, grades):
    """
    Aggregates and counts restaurants by borough for specified grades, excluding those marked as "Missing".
    """
    borough_counts_above_b = collection.aggregate([
        {"$unwind": "$grades"},
        {"$match": {
            "grades.grade": {"$in": grades},
            "borough": {"$ne": "Missing"} 
        }},
        {"$group": {"_id": "$borough", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ])
    
    boroughs = []
    counts = []
    for count in borough_counts_above_b:
        boroughs.append(count['_id'])
        counts.append(count['count'])

    grades_str = ', '.join(grades) 
    title = f"Number of Restaurants with Grade(s) {grades_str} in Each Borough"

    visualizations.plot_borough_counts(boroughs, counts, title)


def find_top_restaurants_and_plot_locations(collection, n):
    """
    Identifies the top n restaurants based on their average grade score and plots their locations.
    """
    top_restaurants = collection.aggregate([
        {"$unwind": "$grades"},
        {"$group": {
            "_id": {
                "name": "$name",
                "location": "$address.coord"
            },
            "averageScore": {"$avg": "$grades.score"}
        }},
        {"$sort": {"averageScore": -1}},
        {"$limit": n}
    ])

    restaurant_names = []
    locations = []
    for restaurant in top_restaurants:
        restaurant_names.append(restaurant['_id']['name'])
        locations.append(restaurant['_id']['location']) 

    visualizations.plot_restaurant_locations_with_basemap(locations, restaurant_names)


def count_restaurants_with_grades_and_plot(collection, grades):
    """
    Counts the total number of restaurants for given grades and plots the count.
    """
    query = {"grades.grade": {"$in": grades}}
    
    grades_count = collection.count_documents(query)
    print(grades_count)

    visualizations.plot_grade_count(grades, grades_count)

    

def find_cuisine(collection, cuisine, borough, grade, n=5):
    """
    Finds up to n restaurants of a specific cuisine in a borough with a certain grade and plots their locations.
    """
    query = {
        "borough": borough,
        "cuisine": cuisine,
        "grades.grade": grade 
    }
    
    cuisine_loc = collection.find(query, {'_id': 0, 'name': 1, 'address': 1, 'grades.$': 1}).limit(n)

    results = []
    for loc in cuisine_loc:
        grade_score = loc['grades'][0]['score'] if loc.get('grades') else None
        results.append({
            'name': loc['name'],
            'address': loc['address'],
            'grade_score': grade_score
        })

    locations = []
    res_names = []
    for result in results:
        locations.append(result['address']['coord'])
        res_names.append(result['name'])
        print(result)
    
    visualizations.plot_restaurant_locations_with_basemap(locations, res_names)


def count_restaurants(collection, grade, cuisines, borough):
    """
    Counts restaurants by cuisine in a borough with a specific grade, calculates average scores, and visualizes results.
    """
    if not isinstance(cuisines, list):
        cuisines = [cuisines]

    count_by_cuisine = {}
    grades_sum_by_cuisine = {}

    for cuisine in cuisines:
        query = {
            "borough": borough,
            "cuisine": cuisine,
            "grades.grade": grade
        }
        restaurants = collection.find(query)

        count = 0
        grades_sum = 0
        for restaurant in restaurants:
            for grade_entry in restaurant['grades']:
                if grade_entry['grade'] == grade:
                    count += 1
                    grades_sum += grade_entry['score']

        count_by_cuisine[cuisine] = count
        grades_sum_by_cuisine[cuisine] = grades_sum

    for cuisine in cuisines:
        average_grade = grades_sum_by_cuisine[cuisine] / count_by_cuisine[cuisine] if count_by_cuisine[cuisine] > 0 else 0
        print(f"Cuisine: {cuisine}, Count: {count_by_cuisine[cuisine]}, Average Grade: {average_grade}")
    
    visualizations.plot_res(count_by_cuisine, grades_sum_by_cuisine)


def find_improved_restaurants(collection):
    """
    Finds restaurants that have improved their score by at least 10 points between their first and last recorded grades.
    """
    return ccollection.aggregate([
    {"$addFields": {
        "firstGradeScore": {"$arrayElemAt": ["$grades.score", -1]},
        "lastGradeScore": {"$arrayElemAt": ["$grades.score", 0]},
    }},
    {"$addFields": {
        "scoreImprovement": {"$subtract": ["$lastGradeScore", "$firstGradeScore"]}
    }},
    {"$match": {"scoreImprovement": {"$gte": 10}}},
    {"$group": {
        "_id": {
            "name": "$name",
            "scoreImprovement": "$scoreImprovement"
        }}},
    {"$limit": 10},
    {"$sort": {"_id.scoreImprovement": -1}}
])


def count_cuisines(collection):
    """
    Counts the number of restaurants for each cuisine, limiting the results to 10 cuisines.
    """
    return collection.aggregate([
        {"$group": {"_id": "$cuisine", "count": {"$sum": 1}}},
        {"$limit": 10}
    ])

def find_high_grade_restaurants(collection):
    """
    Finds up to 10 restaurants that have never received a grade below 'B'.
    """
    return collection.find({
        "grades.grade": {"$not": {"$in": ["C", "D", "F", "Z"]}}
    }, {"name": 1}).limit(10)

def find_most_grades_restaurant(collection):
    """
    Identifies the single restaurant with the highest number of grade records.
    """
    return collection.aggregate([
        {"$project": {"name": 1, "numberOfGrades": {"$size": "$grades"}}},
        {"$sort": {"numberOfGrades": -1}},
        {"$limit": 1}
    ])

def calculate_average_score_by_borough(collection):
    """
    Calculates the average grade score for restaurants in Brooklyn and Queens.
    """
    return collection.aggregate([
        {"$match": {"borough": {"$in": ["Brooklyn", "Queens"]}}},
        {"$unwind": "$grades"},
        {"$group": {
            "_id": "$borough",
            "averageScore": {"$avg": "$grades.score"}
        }}
    ])