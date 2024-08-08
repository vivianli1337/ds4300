from flask import Flask
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from recommender import Recommender

app = Flask(__name__)
dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/')
recommender = Recommender()

# Define the layout of the dashboard
dash_app.layout = html.Div([
    html.H1('Movie Recommendation Dashboard'),
    html.Div(id='movie-count'),
    dcc.Tabs([
        dcc.Tab(label='Movie-to-Movie', children=[
            dcc.Dropdown(id='movie-dropdown', options=[], placeholder='Select a movie'),
            html.Div(id='movie-recommendations', style={'overflow-x': 'scroll', 'display': 'flex', 'flex-wrap': 'nowrap'})
        ]),
        dcc.Tab(label='Keyword', children=[
            dcc.Input(id='keyword-input', type='text', placeholder='Enter keywords'),
            html.Button('Search', id='keyword-search-button'),
            html.Div(id='keyword-recommendations', style={'overflow-x': 'scroll', 'display': 'flex', 'flex-wrap': 'nowrap'})
        ]),
        dcc.Tab(label='Genre', children=[
            dcc.Dropdown(id='genre-dropdown', options=[], multi=True, placeholder='Select genres'),
            html.Div(id='genre-recommendations', style={'overflow-x': 'scroll', 'display': 'flex', 'flex-wrap': 'nowrap'})
        ]),
        dcc.Tab(label='Year', children=[
            dcc.Dropdown(id='year-dropdown', options=[{'label': int(year), 'value': year} for year in range(1900, 2025)], placeholder='Select a year', style={'width': '150px'}),
            html.Button('Search', id='year-search-button'),
            html.Div(id='year-recommendations', className='movie-container', style={'overflow-x': 'scroll', 'display': 'flex', 'flex-wrap': 'nowrap'})
        ]),
        dcc.Tab(label='Actor', children=[
            dcc.Input(id='actor-input', type='text', placeholder='Enter actor name'),
            html.Button('Search', id='actor-search-button'),
            html.Div(id='actor-recommendations', style={'overflow-x': 'scroll', 'display': 'flex', 'flex-wrap': 'nowrap'})
        ]),
        dcc.Tab(label='Language', children=[
            dcc.Input(id='language-input', type='text', placeholder='Enter language'),
            html.Button('Search', id='language-search-button'),
            html.Div(id='language-recommendations', style={'overflow-x': 'scroll', 'display': 'flex', 'flex-wrap': 'nowrap'})
        ])
    ])
])

# Callback for movie count
@dash_app.callback(
    Output('movie-count', 'children'),
    [Input('movie-dropdown', 'value'),
     Input('keyword-input', 'value'),
     Input('genre-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('actor-input', 'value'),
     Input('language-input', 'value')]
)
def update_movie_count(movie_title, keywords, genres, year, actor, language):
    filtered_movies = recommender.filter_movies(movie_title, keywords, genres, year, actor, language)
    count = len(filtered_movies)
    return f"Movies count: {count}"

# Callback for movie-to-movie recommendation
@dash_app.callback(Output('movie-recommendations', 'children'),
                   Input('movie-dropdown', 'value'))
def update_movie_recommendations(movie_title):
    if movie_title:
        movie_recommendations = recommender.get_movie_recommendations(movie_title)[:20]
        return [html.Div([
            html.Img(src=movie['poster_path'], style={'width': '100px', 'height': '150px'}),
            html.P(movie['title'])
        ], style={'margin': '10px'}) for movie in movie_recommendations]
    return []

# Callback for keyword recommendation
@dash_app.callback(Output('keyword-recommendations', 'children'),
                   Input('keyword-search-button', 'n_clicks'),
                   Input('keyword-input', 'value'))
def update_keyword_recommendations(n_clicks, keywords):
    if n_clicks and keywords:
        keyword_recommendations = recommender.get_keyword_recommendations(keywords)[:20]
        return [html.Div([
            html.Img(src=movie['poster_path'], style={'width': '100px', 'height': '150px'}),
            html.P(movie['title'])
        ], style={'margin': '10px'}) for movie in keyword_recommendations]
    return []

# Callback for genre recommendation
@dash_app.callback(Output('genre-recommendations', 'children'),
                   Input('genre-dropdown', 'value'))
def update_genre_recommendations(genres):
    if genres:
        genre_recommendations = recommender.get_genre_recommendations(genres)[:20]
        return [html.Div([
            html.Img(src=movie['poster_path'], style={'width': '100px', 'height': '150px'}),
            html.P(movie['title'])
        ], style={'margin': '10px'}) for movie in genre_recommendations]
    return []

@dash_app.callback(Output('year-recommendations', 'children'),
                   [Input('year-dropdown', 'value')])
def update_year_recommendations(selected_year):
    if selected_year:
        year_recommendations = recommender.get_year_recommendations(selected_year)[:20]
        return [html.Div([
            html.Img(src=movie['poster_path'], style={'width': '100px', 'height': '150px'}),
            html.P(movie['title'])
        ], style={'margin': '10px'}) for movie in year_recommendations]
    return []


# Callback for actor recommendation
@dash_app.callback(Output('actor-recommendations', 'children'),
                   Input('actor-search-button', 'n_clicks'),
                   Input('actor-input', 'value'))
def update_actor_recommendations(n_clicks, actor):
    if n_clicks and actor:
        actor_recommendations = recommender.get_actor_recommendations(actor)[:20]
        return [html.Div([
            html.Img(src=movie['poster_path'], style={'width': '100px', 'height': '150px'}),
            html.P(movie['title'])
        ], style={'margin': '10px'}) for movie in actor_recommendations]
    return []

# Callback for language recommendation
@dash_app.callback(Output('language-recommendations', 'children'),
                   Input('language-search-button', 'n_clicks'),
                   Input('language-input', 'value'))
def update_language_recommendations(n_clicks, language):
    if n_clicks and language:
        language_recommendations = recommender.get_language_recommendations(language)[:20]
        return [html.Div([
            html.Img(src=movie['poster_path'], style={'width': '100px', 'height': '150px'}),
            html.P(movie['title'])
        ], style={'margin': '10px'}) for movie in language_recommendations]
    return []

# Populate the movie dropdown options
@dash_app.callback(Output('movie-dropdown', 'options'),
                   Input('movie-dropdown', 'value'))
def populate_movie_dropdown(value):
    movies = recommender.get_all_movies()
    return [{'label': movie['title'], 'value': movie['title']} for movie in movies]

# Populate the genre dropdown options
@dash_app.callback(Output('genre-dropdown', 'options'),
                   Input('genre-dropdown', 'value'))
def populate_genre_dropdown(value):
    genres = recommender.get_all_genres()
    return [{'label': genre, 'value': genre} for genre in genres]

# Populate the language dropdown options
@dash_app.callback(Output('language-dropdown', 'options'),
                   Input('language-dropdown', 'value'))
def populate_language_dropdown(value):
    languages = recommender.get_all_languages()
    return [{'label': language, 'value': language} for language in languages]



if __name__ == '__main__':
    app.run(debug=True)