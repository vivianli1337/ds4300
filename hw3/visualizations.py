import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def plot_borough_counts(boroughs, counts, title):
    """
    Plots the number of restaurants in each borough. The data is displayed as a bar chart,
    with each bar representing the count of restaurants in a borough.
    """
    plt.figure(figsize=(10, 6))
    plt.bar(boroughs, counts, color='skyblue')
    plt.title(title)
    plt.xlabel('Borough')
    plt.ylabel('Number of Restaurants')
    plt.xticks(rotation=45)
    plt.show()

def plot_restaurant_locations_with_basemap(locations, restaurant_names):
    """
    Plots the geographic locations of top restaurants on a map using Basemap. Each restaurant
    is represented by a point on the map, labeled with the restaurant's name.
    """
    plt.figure(figsize=(10, 6))
    m = Basemap(projection='merc', llcrnrlat=min(lat for _, lat in locations) - 0.25,
                urcrnrlat=max(lat for _, lat in locations) + 0.25,
                llcrnrlon=min(lon for lon, _ in locations) - 0.25,
                urcrnrlon=max(lon for lon, _ in locations) + 0.25,
                lat_ts=20, resolution='i')
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    m.fillcontinents(color='coral', lake_color='aqua')
    m.drawmapboundary(fill_color='aqua')

    for (lon, lat), name in zip(locations, restaurant_names):
        x, y = m(lon, lat)
        m.plot(x, y, 'o', markersize=6, label=name)

    plt.title("Top Restaurants' Locations")
    plt.legend()
    plt.show()

def plot_res(count_by_cuisine, grades_sum_by_cuisine):
    """
    Plots the relationship between the count of restaurants and their average grade for each cuisine.
    This is represented as a scatter plot, with each point indicating a cuisine's average grade
    against its restaurant count.
    """
    if not count_by_cuisine:
        print("No data to plot.")
        return

    plt.figure(figsize=(10, 6))

    for cuisine, count in count_by_cuisine.items():
        average_grade = grades_sum_by_cuisine[cuisine] / count if count > 0 else 0
        plt.plot(count, average_grade, 'o', label=cuisine)

    plt.title('Count vs. Average Grade for Different Cuisines')
    plt.xlabel('Number of Restaurants')
    plt.ylabel('Average Grade')
    plt.legend(title='Cuisine')
    plt.grid(True)
    plt.show()


def plot_grade_count(grades, count):
    """
    Plots the distribution of restaurants across different grades. This bar chart visualizes the
    count of restaurants corresponding to each grade specified in the input.
    """
    plt.bar(grades, count, color='blue')
    
    plt.xlabel('Grades')
    plt.ylabel('Number of Restaurants')
    plt.title('Number of Restaurants for Each Grade')

    plt.show()




