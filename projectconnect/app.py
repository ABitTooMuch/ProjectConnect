from flask import Flask, render_template

app = Flask(__name__)
 
@app.route('/')
def home():
    return "ABitTooMuchHome"
 
@app.route('/dimitri', methods=['GET'])
def dimitri():
    return "This is Dimitri's Endpoint"

@app.route('/huyhuynh', methods=['GET'])
def huyhuynh():
 	return "This is Huy's Endpoint"
	
 
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=4000)
