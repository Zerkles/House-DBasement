from sqlalchemy import *
from flask import request, Flask

db_string = 'postgres://magda:gessler@localhost:5432/housedb'
db_engine = create_engine(db_string)

app = Flask(__name__)


@app.route('/housedb/<house_id>', methods=['GET'])
def get(house_id):
    response = db_engine.execute(f"SELECT * FROM HOUSE where HouseID={house_id}")

    return str(response)


@app.route('/housedb', methods=['POST'])
def post():
    db_engine.execute('SELECT * FROM HOUSE')
    return 'Hello World!'


@app.route('/housedb', methods=['PUT'])
def put():
    db_engine.execute('SELECT * FROM HOUSE')
    return 'Hello World!'


@app.route('/housedb/<house_id>', methods=['DELETE'])
def delete(house_id):
    db_engine.execute(f'DELETE FROM HOUSE WHERE HouseID = {house_id}')
    return ''


if __name__ == '__main__':
    app.run()
