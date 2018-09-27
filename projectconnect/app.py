from flask import Flask
from database import Database

app = Flask(__name__)

Database.initialize()

@app.route('/')
def home():
    return "ABitTooMuchHome"

@app.route('/dimitri', methods=['GET'])
def dimitri():
    return "This is Dimitri's Endpoint"

@app.route('/huyhuynh', methods=['GET'])
def huyhuynh():
 	return "This is Huy's Endpoint"

@app.route('/monica', methods=['GET'])
def monica():
 	return "This is Monica's Endpoint"

@app.route('/carla', methods=['GET'])
def carla():
	return "This is Carla's Endpoint"

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=4000)


