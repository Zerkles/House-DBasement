from sqlalchemy import *
from flask import request, Flask, send_file
from generator.house_generator import json_to_list, create_image

db_string = 'postgres://magda:gessler@localhost:5432/housedb'
db_engine = create_engine(db_string)

app = Flask(__name__)


@app.route('/housedb/<house_id>', methods=['GET'])
def get(house_id):
    houses = db_engine.execute(f"SELECT * FROM Houses where HouseID={house_id}")
    levels = db_engine.execute(f"SELECT * FROM Levels where HouseID={house_id}")
    roofs = db_engine.execute(f"SELECT * FROM Roofs where HouseID={house_id}")

    result_json = {"houses": [dict(zip(houses.keys(), houses.fetchone()))]}
    result_json.update({"roofs": [dict(zip(roofs.keys(), roofs.fetchone()))]})

    for Level in levels:
        if "Levels" not in result_json.keys():
            result_json.update({"Levels": []})

        result_json["Levels"] += [dict(zip(levels.keys(), Level))]

        doors = db_engine.execute(f"SELECT * FROM Doors where LevelID={Level[0]}")
        for door in doors:
            if "doors" not in result_json.keys():
                result_json.update({"doors": []})

            result_json["doors"] += [dict(zip(doors.keys(), door))]

        windows = db_engine.execute(f"SELECT * FROM Windows where LevelID={Level[0]}")
        for window in windows:
            if "windows" not in result_json.keys():
                result_json.update({"windows": []})

            result_json["windows"] += [dict(zip(windows.keys(), window))]

        blanks = db_engine.execute(f"SELECT * FROM Blanks where LevelID={Level[0]}")
        for blank in blanks:
            if "blanks" not in result_json.keys():
                result_json.update({"blanks": []})

            result_json["blanks"] += [dict(zip(blanks.keys(), blank))]

    return result_json


@app.route('/housedb/<house_id>/image', methods=['GET'])
def get_img(house_id):
    house_json = get(house_id)
    img_url = 'obraz' + str(house_id) + '.png'

    return send_file(img_url, mimetype='image/png')


@app.route('/housedb', methods=['POST'])
def post():
    data_json = request.get_json(True)
    levels_map = dict()

    db_engine.execute(
        f"INSERT INTO Houses(LevelsCount, ImageURL) "
        f"Values{data_json['house']['levelscount'], data_json['house']['imageurl']}")

    houseid = db_engine.execute("SELECT MAX(HouseID) FROM Houses").fetchone()[0]

    db_engine.execute(
        f"INSERT INTO Roofs ({'chimneyscount, houseid'}) "
        f"Values{data_json['house']['chimneyscount'], houseid}")

    for obj in data_json['content']:
        if obj['pos_Y'] not in levels_map.keys():
            db_engine.execute(f"INSERT INTO Levels ({'levelfloor, houseid'}) Values{obj['pos_Y'], houseid}")
            levelid = db_engine.execute("SELECT MAX(LevelID) FROM Levels").fetchone()[0]
            levels_map[obj['pos_Y']] = levelid

        if obj["type"] == "window":
            db_engine.execute(
                f"INSERT INTO Windows ({'levelid, position_x'}) Values{levels_map[obj['pos_Y']], obj['pos_X']}")
        elif obj["type"] == "door":
            db_engine.execute(
                f"INSERT INTO Doors ({'levelid, position_x'}) Values{levels_map[obj['pos_Y']], obj['pos_X']}")
        elif obj["type"] == "blank":
            db_engine.execute(
                f"INSERT INTO Blanks ({'levelid, position_x'}) Values{levels_map[obj['pos_Y']], obj['pos_X']}")
        else:
            raise Exception

    latest_added_houseid = db_engine.execute("SELECT MAX(HouseID) FROM Houses").fetchone()[0]

    # generowanie obrazka
    img_tuple = json_to_list(data_json)
    image_path = create_image(img_tuple[0], img_tuple[1], img_tuple[2], latest_added_houseid)
    ###
    house_json = get(latest_added_houseid)
    house_json["houses"][0]["imageurl"] = image_path
    put(house_json)

    return house_json


@app.route('/housedb', methods=['PUT'])
def put(data_json=None):
    if data_json == None:
        data_json = request.get_json(True)

    for table_name in data_json.keys():
        for obj in data_json[table_name]:
            nameid = table_name[:-1] + 'id'
            nameid = nameid.lower()

            keys = list(obj.keys())
            keys.remove(nameid)

            sets = ""
            for k in keys:
                if type(obj[k]) == str:
                    sets += (k + " = '" + obj[k] + "',")
                else:
                    sets += (k + ' = ' + str(obj[k]) + ',')

            db_engine.execute(f"UPDATE {table_name} SET {sets[:-1]} WHERE {nameid}={obj[nameid]}")

    return get(data_json['houses'][0]['houseid'])


@app.route('/housedb/<house_id>', methods=['DELETE'])
def delete(house_id):
    db_engine.execute(f'DELETE FROM Houses WHERE HouseID = {house_id}')
    db_engine.execute(f"DELETE FROM Roofs where HouseID={house_id}")

    levels = db_engine.execute(f"SELECT * FROM Levels where HouseID={house_id}")

    for level in levels:
        db_engine.execute(f"DELETE FROM Doors where LevelID={level[0]}")
        db_engine.execute(f"DELETE FROM Windows where LevelID={level[0]}")
        db_engine.execute(f"DELETE FROM Blanks where LevelID={level[0]}")

    db_engine.execute(f"DELETE FROM Levels where HouseID={house_id}")

    return {"status": "OK", "message": "Deleted succesfully!"}


if __name__ == '__main__':
    app.run()
