from sqlalchemy import *
from flask import request, Flask
import json

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

    for level in levels:
        if "levels" not in result_json.keys():
            result_json.update({"levels": []})

        result_json["levels"] += [dict(zip(levels.keys(), level))]

        doors = db_engine.execute(f"SELECT * FROM Doors where LevelID={level[0]}")
        for door in doors:
            if "doors" not in result_json.keys():
                result_json.update({"doors": []})

            result_json["doors"] += [dict(zip(doors.keys(), door))]

        windows = db_engine.execute(f"SELECT * FROM Windows where LevelID={level[0]}")
        for window in windows:
            if "windows" not in result_json.keys():
                result_json.update({"windows": []})

            result_json["windows"] += [dict(zip(windows.keys(), window))]

        blanks = db_engine.execute(f"SELECT * FROM Blanks where LevelID={level[0]}")
        for blank in blanks:
            if "blanks" not in result_json.keys():
                result_json.update({"blanks": []})

            result_json["blanks"] += [dict(zip(blanks.keys(), blank))]

    print(result_json)
    return result_json


@app.route('/housedb', methods=['POST'])
def post():
    data_json = request.json

    print(data_json)

    db_engine.execute(f"INSERT INTO House Values({data_json['houses'][0]})")
    db_engine.execute(f"INSERT INTO Roofs Values({data_json['roofs'][0]})")

    for level in data_json['levels']:
        db_engine.execute(f"INSERT INTO Levels Values({level})")
    for door in data_json['doors']:
        db_engine.execute(f"INSERT INTO Levels Values({door})")
    for window in data_json['windows']:
        db_engine.execute(f"INSERT INTO Levels Values({window})")
    for blank in data_json['blanks']:
        db_engine.execute(f"INSERT INTO Levels Values({blank})")

    return get(db_engine.execute("SELECT MAX(HouseID) FROM Houses"))


@app.route('/housedb', methods=['PUT'])
def put():
    #kurła to trzeba na spokojnie pomysleć
    return get(db_engine.execute("SELECT MAX(HouseID) FROM Houses"))


@app.route('/housedb/<house_id>', methods=['DELETE'])
def delete(house_id):

    db_engine.execute(f'DELETE FROM HOUSE WHERE HouseID = {house_id}')
    db_engine.execute(f"DELETE FROM Roofs where HouseID={house_id}")

    levels = db_engine.execute(f"SELECT * FROM Levels where HouseID={house_id}")

    for level in levels:
        db_engine.execute(f"DELETE FROM Doors where LevelID={level[0]}")
        db_engine.execute(f"DELETE FROM Windows where LevelID={level[0]}")
        db_engine.execute(f"DELETE FROM Blanks where LevelID={level[0]}")

    db_engine.execute(f"DELETE FROM Levels where HouseID={house_id}")

    return {"status": "OK", "message": "Deleted succesfully!"}


# if __name__ == '__main__':
#     app.run()

get(1)
