from sqlalchemy import *
from flask import request, Flask

db_string = 'postgres://magda:gessler@localhost:5432/housedb'
db_engine = create_engine(db_string)

app = Flask(__name__)


@app.route('/housedb/<house_id>', methods=['GET'])
def get(house_id):
    houses = db_engine.execute(f"SELECT * FROM Houses where HouseID={house_id}")
    Levels = db_engine.execute(f"SELECT * FROM Levels where HouseID={house_id}")
    roofs = db_engine.execute(f"SELECT * FROM Roofs where HouseID={house_id}")

    result_json = {"houses": [dict(zip(houses.keys(), houses.fetchone()))]}
    print(result_json)
    result_json.update({"roofs": [dict(zip(roofs.keys(), roofs.fetchone()))]})

    for Level in Levels:
        if "Levels" not in result_json.keys():
            result_json.update({"Levels": []})

        result_json["Levels"] += [dict(zip(Levels.keys(), Level))]

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

    print(result_json)
    return result_json


@app.route('/housedb', methods=['POST'])
def post():
    data_json = request.get_json(True)
    print(data_json)

    levels_map = dict()

    db_engine.execute(
        f"INSERT INTO Houses(LevelsCount, ImageURL) Values{data_json['house']['levelscount'], data_json['house']['imageurl']}")

    houseid = db_engine.execute("SELECT MAX(HouseID) FROM Houses").fetchone()[0]

    db_engine.execute(
        f"INSERT INTO Roofs ({'chimneyscount, houseid'}) Values{data_json['house']['chimneyscount'], houseid}")

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

    # db_engine.execute(f"INSERT INTO Roofs Values({data_json['roofs'][0]})")
    #
    # for level in data_json["Levels"]:
    #     keys = str(list(level.keys()))[1:-1].replace("'", "")
    #     values = str(list(level.values()))[1:-1]
    #
    #     db_engine.execute(f"INSERT INTO Levels ({keys + ', houseid'}) Values({values + houseid})")
    #     levelid = db_engine.execute("SELECT MAX(LevelID) FROM Levels").fetchone()[0]
    #
    #     for table in level["content"].keys():
    #         for obj in level["content"][table]:
    #             keys = str(list(obj.keys()))[1:-1].replace("'", "")
    #             values = str(list(obj.values()))[1:-1]
    #
    #             db_engine.execute(f"INSERT INTO {table} ({keys + 'Levelid'}) Values({values + levelid})")

    # for Level in data_json['Levels']:
    #     keys = str(list(Level.keys()))[1:-1].replace("'", "")
    #     values = str(list(Level.values()))[1:-1].replace("'", "")
    #
    #     db_engine.execute(f"INSERT INTO Levels ({keys}) Values({values})")

    return get(db_engine.execute("SELECT MAX(HouseID) FROM Houses").fetchone()[0])


@app.route('/housedb', methods=['PUT'])
def put():
    data_json = request.get_json(True)

    for table in data_json.keys():
        for obj in data_json[table]:

                keys = str(list(obj.keys())[1:])[1:-1].replace("'", "")
                print(keys)
                values = str(list(obj.values())[1:])[1:-1]
                print(values)

                db_engine.execute(f"UPDATE {table}  SET{keys,values} WHERE {table}ID={obj[table+'ID']}")

    return get(db_engine.execute("SELECT MAX(HouseID) FROM Houses").fetchone()[0])


@app.route('/housedb/<house_id>', methods=['DELETE'])
def delete(house_id):
    db_engine.execute(f'DELETE FROM Houses WHERE HouseID = {house_id}')
    db_engine.execute(f"DELETE FROM Roofs where HouseID={house_id}")

    Levels = db_engine.execute(f"SELECT * FROM Levels where HouseID={house_id}")

    for Level in Levels:
        db_engine.execute(f"DELETE FROM Doors where LevelID={Level[0]}")
        db_engine.execute(f"DELETE FROM Windows where LevelID={Level[0]}")
        db_engine.execute(f"DELETE FROM Blanks where LevelID={Level[0]}")

    db_engine.execute(f"DELETE FROM Levels where HouseID={house_id}")

    return {"status": "OK", "message": "Deleted succesfully!"}


if __name__ == '__main__':
    app.run()
