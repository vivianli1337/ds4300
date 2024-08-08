from py2neo import Graph

# Connect to the Neo4j database
graph = Graph("bolt://localhost:7687", auth=("neo4j", "neo4j_password"))

# Query to retrieve songs by The Strokes and their similar songs with artist and album information
query = """
MATCH (s:Song)-[:PERFORMED_BY]->(a:Artist {name: "The Strokes"})
MATCH (s)-[:BELONGS_TO]->(album:Album)
OPTIONAL MATCH (s)-[:SIMILAR_TO]->(similar:Song)
OPTIONAL MATCH (similar)-[:PERFORMED_BY]->(similarArtist:Artist)
OPTIONAL MATCH (similar)-[:BELONGS_TO]->(similarAlbum:Album)
RETURN s.track_name AS song, 
       a.name AS artist,
       album.name AS album,
       collect({track_name: similar.track_name, 
                artist: similarArtist.name, 
                album: similarAlbum.name}) AS similar_songs
"""

results = graph.run(query)

print("Songs by The Strokes and similar songs:")
for record in results:
    song = record['song']
    artist = record['artist']
    album = record['album']
    similar_songs = record['similar_songs']
    
    print(f"Song: {song}")
    print(f"Artist: {artist}")
    print(f"Album: {album}")
    print("Similar songs:")
    
    if similar_songs:
        for similar_song in similar_songs:
            track_name = similar_song['track_name']
            artist = similar_song['artist']
            album = similar_song['album']
            
            print(f"- Track: {track_name}")
            print(f"  Artist: {artist}")
            print(f"  Album: {album}")
            print()
    else:
        print("No similar songs found")
    
    print("---")

# number of nodes
node_count_query = """
MATCH (n)
RETURN count(n) AS NumberOfNodes;
"""

result = graph.run(node_count_query).evaluate()
print("Number of Nodes:", result)


# number of edges
relationship_count_query = """
MATCH ()-[r]->()
RETURN count(r) AS NumberOfEdges;
"""

result = graph.run(relationship_count_query).evaluate()
print("Number of Edges:", result)



