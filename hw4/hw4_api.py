import redis

class GraphAPI:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

    def add_node(self, name, node_type):
        self.redis_client.hset('nodes', name, node_type)

    def add_edge(self, name1, name2, edge_type):
        self.redis_client.hset(f'edges:{name1}', name2, edge_type)

    def get_adjacent(self, name, node_type=None, edge_type=None):
        adjacent_nodes = self.redis_client.hkeys(f'edges:{name}')

        if node_type:
            adjacent_nodes = [node for node in adjacent_nodes if self.redis_client.hget('nodes', node) == node_type]

        if edge_type:
            adjacent_nodes = [node for node in adjacent_nodes if self.redis_client.hget(f'edges:{name}', node) == edge_type]

        return adjacent_nodes

    def get_recommendations(self, name):
        known_people = self.get_adjacent(name)
        recommendations = set()

        for person in known_people:
            if person != name:
                books_purchased = self.get_adjacent(person, node_type='Book', edge_type='bought')
                recommendations.update(books_purchased)

        user_books = set(self.get_adjacent(name, node_type='Book', edge_type='bought'))
        recommendations -= user_books

        return list(recommendations)
    
    def delete_node(self, name):
        self.redis_client.hdel('nodes', name)
        
        self.redis_client.delete(f'edges:{name}')


