from py2neo import Graph, Node, Relationship
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances

graph = Graph("bolt://localhost:7687", auth=("neo4j", "neo4j_password"))

data = pd.read_csv("/home/daniel/Documents/Spring2024/DS4300/HW5/spotify.csv")
data = data.dropna()

# Make sure to uncomment this when creating a graph from scratch
# graph.run("CREATE CONSTRAINT constraint_Artist_name FOR (a:Artist) REQUIRE a.name IS UNIQUE")
# graph.run("CREATE CONSTRAINT constraint_Album_name FOR (al:Album) REQUIRE al.name IS UNIQUE")
# graph.run("CREATE CONSTRAINT constraint_Genre_name FOR (g:Genre) REQUIRE g.name IS UNIQUE")

#10,000 entries from the data were sampled along with all of the songs by the Strokes
strokes_songs = data[data["artists"].str.contains("The Strokes")]
sampled_data = data[~data["track_id"].isin(
    strokes_songs["track_id"])].sample(n=10000, random_state=42)
sampled_data = pd.concat([sampled_data, strokes_songs])
sampled_data = sampled_data.reset_index(drop=True)

features = ["popularity", "duration_ms", "danceability", "energy", "key", "loudness", "mode", "speechiness",
            "acousticness", "instrumentalness", "liveness", "valence", "tempo", "time_signature"]

distances = euclidean_distances(sampled_data[features])

similar_songs = {}
for i, row in sampled_data.iterrows():
    song_id = row["track_id"]
    artist = row["artists"]
    mask = (sampled_data["artists"] != artist) & (
        sampled_data["track_id"] != song_id)
    indices = mask.values.nonzero()[0]
    song_distances = distances[i, indices]
    top_indices = indices[song_distances.argsort()[:5]]

    similar_songs[song_id] = sampled_data.iloc[top_indices]["track_id"].tolist()


for _, row in sampled_data.iterrows():
    song = Node("Song",
                track_id=row["track_id"],
                track_name=row["track_name"],
                popularity=row["popularity"],
                duration_ms=row["duration_ms"],
                explicit=row["explicit"],
                danceability=row["danceability"],
                energy=row["energy"],
                key=row["key"],
                loudness=row["loudness"],
                mode=row["mode"],
                speechiness=row["speechiness"],
                acousticness=row["acousticness"],
                instrumentalness=row["instrumentalness"],
                liveness=row["liveness"],
                valence=row["valence"],
                tempo=row["tempo"],
                time_signature=row["time_signature"]
                )
    graph.create(song)

    artists = row["artists"].split(";")
    for artist_name in artists:
        artist = Node("Artist", name=artist_name)
        graph.merge(artist, "Artist", "name")
        graph.create(Relationship(song, "PERFORMED_BY", artist))

    album = Node("Album", name=row["album_name"])
    graph.merge(album, "Album", "name")
    graph.create(Relationship(song, "BELONGS_TO", album))

    genre = Node("Genre", name=row["track_genre"])
    graph.merge(genre, "Genre", "name")
    graph.create(Relationship(song, "HAS_GENRE", genre))

    for artist_name in artists:
        artist = Node("Artist", name=artist_name)
        graph.merge(artist, "Artist", "name")
        graph.create(Relationship(artist, "RELEASED", album))


for song_id, similar_ids in similar_songs.items():
    song = graph.nodes.match("Song", track_id=song_id).first()
    for similar_id in similar_ids:
        similar_song = graph.nodes.match("Song", track_id=similar_id).first()
        if song and similar_song:
            graph.create(Relationship(song, "SIMILAR_TO", similar_song))

print("Data import and similarity relationships created.")

"""
Data Model:
    Nodes:
    Album (attribute: name)
    Artist (attribute: name)
    Song (attributes: track_id, track_name, popularity, duration_ms, explicit, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature)
    Genre (attribute: name)

    Relationships:
    Song BELONGS_TO Album
    Song PERFORMED_BY Artist
    Song HAS_GENRE Genre
    Song SIMILAR_TO Song

The recomendation algorithm is based on the euclidean distance between the features of the songs. 
The top 5 similar songs that are not by the same artist and not the song itself
are found for each song and a SIMILAR_TO relationship is created between them.

Number of Nodes: 25787
Number of Edges: 94697

Song: Someday
Artist: The Strokes
Album: Is This It
Similar songs:
- Track: Into Hell's Mouth We March
  Artist: Vanna
  Album: A New Hope

- Track: god's chariots
  Artist: Oklou
  Album: Galore

- Track: The Last of Us
  Artist: Gustavo Santaolalla
  Album: The Last of Us

- Track: Arcade
  Artist: Duncan Laurence
  Album: Arcade

- Track: waves
  Artist: 53 Thieves
  Album: waves


Query for the graph in the Slide:
MATCH (s)-[:HAS_GENRE]->(genre:Genre)
OPTIONAL MATCH (s)-[:SIMILAR_TO]->(similar:Song)
OPTIONAL MATCH (similar)-[:PERFORMED_BY]->(similarArtist:Artist)
OPTIONAL MATCH (similar)-[:BELONGS_TO]->(similarAlbum:Album)
OPTIONAL MATCH (similar)-[:HAS_GENRE]->(similarGenre:Genre)
RETURN s AS song, 
       a AS artist,
       album AS album,
       genre AS genre,
       collect({song: similar, artist: similarArtist, album: similarAlbum, genre: similarGenre}) AS similar_songs
LIMIT 5

"""