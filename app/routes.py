from app import app

@app.route('/')
@app.route('/index')
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