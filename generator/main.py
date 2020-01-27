import generator.house_generator as generator
import json


# generator.create_image([['w', 'w', 'd', 'd', 'b'],
#                         ['w', 'w', 'b', 'b', 'b'],
#                         ['w', 'w', 'b', 'w', 'd']], chimneys=2, roof=True)


with open('json_data2.json') as f:
    data = json.load(f)


house = generator.json_to_list(data)

generator.create_image(house[0], house[1], house[2])

