import json

with open('/Users/vivianli/Documents/ds4300/data/restaurants.json', 'r') as file:
    data = file.readlines()

# Remove any newline characters and concatenate the objects with commas
json_content = '[' + ','.join(data) + ']'

# Load the corrected content as JSON
corrected_data = json.loads(json_content)

# Write the corrected data to a new file
with open('/Users/vivianli/Documents/ds4300/data/corrected_file.json', 'w') as file:
    json.dump(corrected_data, file, indent=2)
