import json
import requests

def get_data(filename):
    with open(filename, 'r') as file_data:
        return json.loads(file_data.read(), encoding='utf-8')


def save_data(filename, data):
    with open(filename, 'w') as file_data:
        json.dump(data, file_data, indent=4)

my_house = 'r1/bdb/wwb/bbb/bbb/wwb'  # house example

def create_house(house:str):
    data = dict()
    chimney = int(house[1])
    roof = house[0] == 'r'

    house = house.split('/')
    house.pop(0)
    width = len(house[0])
    lvl_cnt = len(house)

    houses = {
        "levelscount": lvl_cnt,
        "width": width,
        "imageurl": "asdsa",
        "chimneyscount": chimney,
        "roof": roof
    }

    content = []

    print(house)

    for i in range(len(house)):
        for j in range(len(house[i])):
            if house[i][j] == 'b':
                type = 'blank'
            elif house[i][j] == 'w':
                type = 'window'
            elif house[i][j] == 'd':
                type = 'door'

            content.append({"type":type, "pos_X":j, "pos_Y":i})

    data = {"house": houses, "content": content}
    print(data)
    save_data("json_data.json", data)
    r = requests.post("http://127.0.0.1:5000/housedb", data=json.dumps(data))

print('format:')
print('r0/dw/bb/ww')
print('house with roof, without chimney and three floors')
print('r -> there is roof')
print('_ -> no roof')
print('d -> numebr of chimneys 0/1/2')
print('floors separeted by /')

my_house = input()

create_house(my_house)
