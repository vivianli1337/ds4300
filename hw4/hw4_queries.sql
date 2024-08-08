# a. What is the sum of all book prices? Give just the sum.
SELECT SUM(COALESCE(num_value, 0)) AS total_book_prices
FROM node_props
WHERE propkey = 'price';

# b. Who does spencer know? Give just their names.
SELECT np.string_value AS person_name
FROM edge e
JOIN node_props np ON e.out_node = np.node_id
WHERE e.type = 'knows' AND e.in_node = (
    SELECT node_id FROM node WHERE type = 'Person' AND node_id = (
        SELECT node_id FROM node_props WHERE string_value = 'Spencer' AND propkey = 'name'
    )
);

# c. What books did Spencer buy? Give title and price.
SELECT np_title.string_value AS title, np_price.num_value AS price
FROM edge AS e
JOIN node_props AS np_title ON e.out_node = np_title.node_id
JOIN node_props AS np_price ON e.out_node = np_price.node_id
WHERE e.type = 'bought'
AND e.in_node = 2
AND np_title.propkey = 'title'
AND np_price.propkey = 'price';

# d. Who knows each other? Give just a pair of names.
SELECT np1.string_value AS person1, np2.string_value AS person2
FROM edge e1
JOIN edge e2 ON e1.out_node = e2.in_node AND e1.in_node = e2.out_node
JOIN node_props np1 ON e1.out_node = np1.node_id
JOIN node_props np2 ON e1.in_node = np2.node_id
WHERE e1.type = 'knows' AND e2.type = 'knows' AND np1.node_id < np2.node_id;

# e. What books were purchased by people who Spencer knows? Exclude books that Spencer already owns.
SELECT DISTINCT np_title.string_value AS recommended_books
FROM edge AS e1
JOIN edge AS e2 ON e1.out_node = e2.in_node
JOIN node_props AS np_spencer ON e1.in_node = np_spencer.node_id
JOIN node_props AS np_title ON e2.out_node = np_title.node_id
JOIN node AS n_spencer ON np_spencer.node_id = n_spencer.node_id
JOIN node AS n_title ON np_title.node_id = n_title.node_id
LEFT JOIN edge AS e3 ON e3.out_node = e2.out_node AND e3.in_node = 2
WHERE e1.type = 'knows'
AND e2.type = 'bought'
AND np_spencer.propkey = 'name' AND np_spencer.string_value = 'Spencer'
AND n_spencer.type = 'Person'
AND n_title.type = 'Book'
AND e3.edge_id IS NULL;

