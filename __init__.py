from datetime import timedelta
from txtplz import app
app.config['MONGODB_SETTINGS'] = {'DB': "txtplz"}
app.config['SECRET_KEY'] = 'DebugSecret'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=3600)

app.jinja_env.autoescape = True








if __name__ == '__main__':
	app.run(debug=True)
