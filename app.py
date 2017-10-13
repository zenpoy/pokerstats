import os
from flask import Flask, request, jsonify
from mongoengine import *
import datetime

app = Flask(__name__)

mongodb_uri = os.environ.get('MONGODB_URI', 'localhost:27017')

connect("pokerstats", host=mongodb_uri)

class Player(Document):
	name = StringField(required=True, unique=True, max_length=200)


class Record(Document):
	player = ReferenceField("Player", required=True)
	game = ReferenceField("Game", required=True)
	cash_in = FloatField()
	good_all_in = ListField(field=DateTimeField)
	bad_all_in = ListField(field=DateTimeField)
	cash_out = FloatField()


class Game(Document):
	name = StringField(max_length=200)
	date = DateTimeField()
	cash = FloatField()


@app.route('/', methods=['GET'])
@app.route('/players', methods=['GET'])
def get_players():
	return Player.objects.to_json()

@app.route('/players/<player_id>', methods=['GET'])
def get_player(player_id):
	p = Player.objects(id=player_id)
	return p.to_json(), 200

@app.route('/players', methods=['POST'])
def create_player():
	# TODO: add check for is json
	json_data = request.get_json()
	p = Player(**json_data)
	try:
		p.save()
	except NotUniqueError as e:
		return jsonify({'error' : e.message}), 200
	return p.to_json(), 201

@app.route('/players/<player_id>', methods=['DELETE'])
def delete_player(player_id):
	Player.objects(id=player_id).delete()
	return jsonify({}), 200

@app.route('/players/<player_id>', methods=['PUT'])
def update_player(player_id):
	# TODO: add check for is json
	json_data = request.get_json()
	p = Player.objects(id=player_id)
	p.update(**json_data)
	return p.to_json(), 200

@app.route('/games', methods=['GET'])
def get_games():
	return Game.objects.to_json()

@app.route('/games/<game_id>', methods=['GET'])
def get_game(game_id):
	p = Game.objects(id=game_id)
	return p.to_json(), 200

@app.route('/games', methods=['POST'])
def create_game():
	# TODO: add check for is json
	json_data = request.get_json()
	p = Game(**json_data)
	try:
		p.save()
	except NotUniqueError as e:
		return jsonify({'error' : e.message}), 200
	return p.to_json(), 201

@app.route('/games/<game_id>', methods=['DELETE'])
def delete_game(game_id):
	Game.objects(id=game_id).delete()
	return jsonify({}), 200

@app.route('/games/<game_id>', methods=['PUT'])
def update_game(game_id):
	# TODO: add check for is json
	json_data = request.get_json()
	p = Game.objects(id=game_id)
	p.update(**json_data)
	return p.to_json(), 200

@app.route('/records', methods=['GET'])
def get_records():
	return Record.objects.to_json()

@app.route('/records/<record_id>', methods=['GET'])
def get_record(record_id):
	p = Record.objects(id=record_id)
	return p.to_json(), 200

@app.route('/records', methods=['POST'])
def create_record():
	# TODO: add check for is json
	json_data = request.get_json()
	p = Record(**json_data)
	try:
		p.save()
	except NotUniqueError as e:
		return jsonify({'error' : e.message}), 200
	return p.to_json(), 201

@app.route('/records/<record_id>', methods=['DELETE'])
def delete_record(record_id):
	Record.objects(id=record_id).delete()
	return jsonify({}), 200

@app.route('/records/<record_id>', methods=['PUT'])
def update_record(record_id):
	# TODO: add check for is json
	json_data = request.get_json()
	p = Record.objects(id=record_id)
	p.update(**json_data)
	return p.to_json(), 200

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

    # connect to the mongodb database