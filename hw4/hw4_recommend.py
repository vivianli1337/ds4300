from hw4_api import GraphAPI


def main():
    graph_api = GraphAPI()

    graph_api.add_node('Emily', 'Person')
    graph_api.add_node('Spencer', 'Person')
    graph_api.add_node('Brendan', 'Person')
    graph_api.add_node('Trevor', 'Person')
    graph_api.add_node('Paxtyn', 'Person')

    graph_api.add_node('Cosmos', 'Book')
    graph_api.add_node('Database Design', 'Book')
    graph_api.add_node('The Life of Cronkite', 'Book')
    graph_api.add_node('DNA & You', 'Book')

    graph_api.add_edge('Emily', 'Spencer', 'knows')
    graph_api.add_edge('Spencer', 'Emily', 'knows')
    graph_api.add_edge('Spencer', 'Brendan', 'knows')

    graph_api.add_edge('Spencer', 'Cosmos', 'bought')
    graph_api.add_edge('Spencer', 'Database Design', 'bought')

    graph_api.add_edge('Emily', 'Database Design', 'bought')

    graph_api.add_edge('Brendan', 'Database Design', 'bought')
    graph_api.add_edge('Brendan', 'DNA & You', 'bought')

    graph_api.add_edge('Trevor', 'Database Design', 'bought')
    graph_api.add_edge('Brendan', 'Cosmos', 'bought')

    graph_api.add_edge('Paxtyn', 'Database Design', 'bought')
    graph_api.add_edge('Paxtyn', 'The Life of Cronkite', 'bought')

    adjacent_nodes = graph_api.get_adjacent('Spencer', node_type='Person', edge_type='knows')
    print(f"Friends of Spencer: {adjacent_nodes}")

    recommendations = graph_api.get_recommendations('Spencer')
    print(f"Book recommendations for Spencer: {recommendations}")

if __name__ == "__main__":
    main()   