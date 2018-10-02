from flask import Flask, render_template
import clock
from weather import Weather, Unit




app = Flask(__name__,template_folder='./templates')
 
@app.route('/')
def home():
    return "ABitTooMuchHome"
 
@app.route('/dimitri', methods=['GET'])
def dimitri():
    return "This is Dimitri's Endpoint"


@app.route('/user/<username>', methods=['GET'])
def huy(username):
#	template = env.get_template('index.html')
#	return (template.render(uesrname = username))
	return render_template('login.html', time=clock.now(), timezone=clock.localtimezone)

@app.route('/timezones', methods=['GET'])
def timezone():
	return "..............."

@app.route('/monica/<username>', methods=['GET'])
def monica(username):
 	return render_template('index.html', username=username)
	
@app.route('/carla', methods=['GET'])
def carla():
	weather = Weather(unit=Unit.CELSIUS)
	lookup=weather.lookup(560743)
	condition = lookup.condition
	print(condition.text)
	return condition.text
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=4000)
