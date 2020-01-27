from PIL import ImageDraw, Image
from typing import List


def create_image(house_model: List[List[chr]] = None, chimneys: int = 0, roof: bool = False, house_id: int = 0):
    print(house_model)
    height = 40 * len(house_model)
    if roof or chimneys > 0:
        height += 40
    width = 40 * len(house_model[0])
    print(height, width)

    img = Image.new('1', (width, height), 1)
    draw = ImageDraw.Draw(img)
    floor_id_max = int((height/40) - 1)
    floor_id_current = 0
    print(floor_id_current, floor_id_max)
    segment_id = 0
    for row in house_model:
        for segment in row:
            if segment == 'w':
                draw.rectangle(((10 + 40*segment_id, 10 + 40 * (floor_id_max-floor_id_current)),
                                (30 + 40*segment_id, 30 + 40 * (floor_id_max-floor_id_current))))
            elif segment == 'd':
                draw.rectangle(((10 + 40*segment_id, 10 + 40 * (floor_id_max-floor_id_current)),
                                (30 + 40*segment_id, 39 + 40 * (floor_id_max-floor_id_current))))
                draw.line(((12 + 40*segment_id, 25 + 40 * (floor_id_max-floor_id_current)),
                           (15 + 40*segment_id, 25 + 40 * (floor_id_max-floor_id_current))))
                draw.line(((15 + 40*segment_id, 25 + 40 * (floor_id_max-floor_id_current)),
                           (15 + 40*segment_id, 26 + 40 * (floor_id_max-floor_id_current))))
            elif segment == 'b':
                pass
            else:
                print('Wrong data in ')
            segment_id += 1
        floor_id_current += 1
        segment_id = 0

    for i in range(chimneys):
        draw.line(((0, height-(len(house_model)*40)), (width, height-(len(house_model)*40))))
        if i == 0:
            draw.rectangle(((width-25, 15), (width-20, 40)), fill='black')
        if i == 1:
            draw.rectangle(((15, 15), (20, 40)), fill='black')

    if roof:
        draw.polygon(((2, height-(len(house_model)*40)), (width-1, height-(len(house_model)*40)), (int(width/2), 1)),
                     fill='white')
        draw.line(((0, height-(len(house_model)*40)), (width, height-(len(house_model)*40))))
        draw.line(((0, height-(len(house_model)*40)), (int(width/2), 0)))
        draw.line(((int(width/2), 0), (width, height-(len(house_model)*40))))

    filename = 'obraz' + str(house_id) + '.png'
    img.save(filename)

    img_generated = Image.open(filename)

    return img_generated.filename


def json_to_list(json_) -> (List[List[chr]], int, bool):
    levels = int(json_['house']['levelscount'])
    width = int(json_['house']['width'])
    chimney = int(json_['house']['chimneyscount'])
    roof = bool(json_['house']['roof'])
    res = [['' for _ in range(width)] for _ in range(levels)]

    for item in json_['content']:
        res[item['pos_Y']][item['pos_X']] = item['type'][0]

    return res, chimney, roof

